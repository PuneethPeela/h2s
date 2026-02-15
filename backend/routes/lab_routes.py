from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.ai_service import ai_service
from mongo_models import LabReport
import os

lab_bp = Blueprint('lab', __name__)

@lab_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_report():
    user_id = get_jwt_identity()
    if 'file' not in request.files:
        return jsonify({"msg": "No file part"}), 400
    
    file = request.files['file']
    file_bytes = file.read()
    
    # OCR Extraction via AWS Textract
    extracted_text = ai_service.extract_lab_data(file_bytes)
    
    # Use AI to simplify the results
    simplified_explanation = ai_service.get_chat_response(
        f"Simplify this lab report and highlight concern areas: {extracted_text[:2000]}"
    )
    
    # Save to MongoDB
    report = LabReport(
        user_id=user_id,
        file_name=file.filename,
        extracted_data={"raw_text": extracted_text},
        summary=simplified_explanation,
        health_score="Normal" # Mock logic
    )
    report.save()
    
    return jsonify({
        "msg": "Report processed successfully",
        "summary": simplified_explanation,
        "health_score": "Normal"
    }), 200

@lab_bp.route('/reports', methods=['GET'])
@jwt_required()
def get_reports():
    user_id = get_jwt_identity()
    reports = LabReport.objects(user_id=user_id).order_by('-uploaded_at')
    return jsonify([{
        "id": str(r.id),
        "file_name": r.file_name,
        "summary": r.summary,
        "health_score": r.health_score,
        "date": r.uploaded_at.isoformat()
    } for r in reports]), 200
