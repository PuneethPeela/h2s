from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100))
    dob = db.Column(db.Date)
    gender = db.Column(db.String(20))
    blood_type = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class MedicalHistory(db.Model):
    __tablename__ = 'medical_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    condition = db.Column(db.String(255), nullable=False)
    diagnosis_date = db.Column(db.Date)
    status = db.Column(db.String(50)) # e.g., active, resolved

class Prescription(db.Model):
    __tablename__ = 'prescriptions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    drug_name = db.Column(db.String(255), nullable=False)
    dosage = db.Column(db.String(100))
    frequency = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

class Reminder(db.Model):
    __tablename__ = 'reminders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescriptions.id'), nullable=False)
    reminder_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending') # pending, taken, skipped

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_name = db.Column(db.String(255))
    reason = db.Column(db.Text)
    appointment_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255))
    status = db.Column(db.String(50), default='scheduled')
