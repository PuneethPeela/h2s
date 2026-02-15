from mongoengine import Document, StringField, ListField, DictField, DateTimeField, ReferenceField
from datetime import datetime

class MedicalKnowledge(Document):
    meta = {'collection': 'medical_knowledge'}
    disease_name = StringField(required=True, unique=True)
    symptoms = ListField(StringField())
    treatments = ListField(StringField())
    lifestyle_advice = StringField()
    risk_factors = ListField(StringField())

class ChatHistory(Document):
    meta = {'collection': 'chat_history'}
    user_id = StringField(required=True)
    session_id = StringField(required=True)
    messages = ListField(DictField()) # [{role, text, timestamp}]
    created_at = DateTimeField(default=datetime.utcnow)

class LabReport(Document):
    meta = {'collection': 'lab_reports'}
    user_id = StringField(required=True)
    file_name = StringField()
    extracted_data = DictField()
    summary = StringField()
    health_score = StringField()
    uploaded_at = DateTimeField(default=datetime.utcnow)
