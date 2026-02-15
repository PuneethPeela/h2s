from flask import Blueprint, request, jsonify
from extensions import db, jwt
from models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import re

auth_bp = Blueprint('auth', __name__)

def is_valid_email(email):
    # Standard email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email', '')
    
    if not is_valid_email(email):
        return jsonify({"msg": "Invalid email format"}), 400
        
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400
    
    new_user = User(
        email=data['email'],
        full_name=data.get('full_name'),
        gender=data.get('gender'),
        blood_type=data.get('blood_type')
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return jsonify(access_token=access_token), 200
    
    return jsonify({"msg": "Invalid email or password"}), 401

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({
        "email": user.email,
        "full_name": user.full_name,
        "dob": user.dob.isoformat() if user.dob else None,
        "gender": user.gender,
        "blood_type": user.blood_type
    }), 200
