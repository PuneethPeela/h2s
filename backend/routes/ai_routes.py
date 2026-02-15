from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.ai_service import ai_service
from services.symptom_service import symptom_checker
from mongo_models import ChatHistory
import uuid

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    data = request.get_json()
    user_id = get_jwt_identity()
    user_message = data.get('message')
    session_id = data.get('session_id', str(uuid.uuid4()))
    
    # Get previous context from MongoDB
    chat_log = ChatHistory.objects(session_id=session_id).first()
    context = ""
    if chat_log:
        context = " ".join([m['text'] for m in chat_log.messages[-3:]]) # last 3 messages
    
    ai_response = ai_service.get_chat_response(user_message, context)
    
    # Save to MongoDB
    if not chat_log:
        chat_log = ChatHistory(user_id=user_id, session_id=session_id, messages=[])
    
    chat_log.messages.append({"role": "user", "text": user_message})
    chat_log.messages.append({"role": "assistant", "text": ai_response})
    chat_log.save()
    
    return jsonify({
        "response": ai_response,
        "session_id": session_id
    }), 200

@ai_bp.route('/symptom-check', methods=['POST'])
@jwt_required()
def symptom_check():
    data = request.get_json()
    symptoms = data.get('symptoms', [])
    result = symptom_checker.predict(symptoms)
    return jsonify(result), 200
