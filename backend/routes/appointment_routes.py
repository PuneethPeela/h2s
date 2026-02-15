from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Appointment
from datetime import datetime

appointment_bp = Blueprint('appointments', __name__)

@appointment_bp.route('/', methods=['POST'])
@jwt_required()
def create_appointment():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        new_appointment = Appointment(
            user_id=user_id,
            doctor_name=data['doctor_name'],
            specialty=data.get('specialty'),
            appointment_time=datetime.fromisoformat(data['appointment_time']),
            location=data.get('location'),
            reason=data.get('reason'),
            status='scheduled'
        )
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({"msg": "Appointment scheduled successfully", "id": new_appointment.id}), 201
    except Exception as e:
        return jsonify({"msg": str(e)}), 400

@appointment_bp.route('/', methods=['GET'])
@jwt_required()
def get_appointments():
    user_id = get_jwt_identity()
    appointments = Appointment.query.filter_by(user_id=user_id).order_by(Appointment.appointment_time.asc()).all()
    
    return jsonify([{
        "id": a.id,
        "doctor_name": a.doctor_name,
        "specialty": a.specialty,
        "appointment_time": a.appointment_time.isoformat(),
        "location": a.location,
        "reason": a.reason,
        "status": a.status
    } for a in appointments]), 200
