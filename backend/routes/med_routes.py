from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Prescription, Reminder
from datetime import datetime, timedelta

meds_bp = Blueprint('meds', __name__)

@meds_bp.route('/prescriptions', methods=['POST'])
@jwt_required()
def add_prescription():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    new_presc = Prescription(
        user_id=user_id,
        drug_name=data['drug_name'],
        dosage=data.get('dosage'),
        frequency=data.get('frequency'),
        start_date=datetime.fromisoformat(data['start_date']) if data.get('start_date') else None,
        end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None
    )
    db.session.add(new_presc)
    db.session.flush() # Get ID
    
    # Automatically schedule first reminder
    reminder = Reminder(
        user_id=user_id,
        prescription_id=new_presc.id,
        reminder_time=datetime.utcnow() + timedelta(hours=4), # Simple mock logic
        status='pending'
    )
    db.session.add(reminder)
    db.session.commit()
    
    return jsonify({"msg": "Prescription and reminder added"}), 201

@meds_bp.route('/reminders', methods=['GET'])
@jwt_required()
def get_reminders():
    user_id = get_jwt_identity()
    reminders = Reminder.query.filter_by(user_id=user_id, status='pending').all()
    return jsonify([{
        "id": r.id,
        "drug_name": Prescription.query.get(r.prescription_id).drug_name,
        "time": r.reminder_time.isoformat(),
        "status": r.status
    } for r in reminders]), 200

@meds_bp.route('/reminders/<int:reminder_id>/mark-taken', methods=['POST'])
@jwt_required()
def mark_taken(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if not reminder:
        return jsonify({"msg": "Reminder not found"}), 404
    
    reminder.status = 'taken'
    db.session.commit()
    return jsonify({"msg": "Medication marked as taken"}), 200
