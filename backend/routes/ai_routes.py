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
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        user_message = data.get('message', '')
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Get previous context from MongoDB (optimized with limit)
        try:
            chat_log = ChatHistory.objects(session_id=session_id).first()
            context = ""
            if chat_log and chat_log.messages:
                context = " ".join([m.get('text', '') for m in chat_log.messages[-3:]])
        except Exception as mongo_err:
            # MongoDB connection issue - continue without context
            context = ""
            chat_log = None
        
        # Get AI response with error handling
        try:
            ai_response = ai_service.get_chat_response(user_message, context)
        except Exception as ai_err:
            # Fallback response if OpenAI fails
            ai_response = ("I'm currently operating in demo mode. "
                          "For a fully functional AI assistant, please configure the OpenAI API key. "
                          f"I understand you mentioned: '{user_message[:50]}...'. "
                          "In production, I would provide detailed medical information and guidance.")
        
        # Save to MongoDB (optional, skip if connection fails)
        try:
            if not chat_log:
                chat_log = ChatHistory(user_id=user_id, session_id=session_id, messages=[])
            
            chat_log.messages.append({"role": "user", "text": user_message})
            chat_log.messages.append({"role": "assistant", "text": ai_response})
            chat_log.save()
        except Exception:
            pass  # Continue even if MongoDB save fails
        
        return jsonify({
            "response": ai_response,
            "session_id": session_id
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_bp.route('/symptom-check', methods=['POST'])
@jwt_required()
def symptom_check():
    data = request.get_json()
    symptoms = data.get('symptoms', [])
    result = symptom_checker.predict(symptoms)
    return jsonify(result), 200
