from flask import Blueprint, request, jsonify
from server.app.extensions import db
from server.app.models import MedicalRecord, Patient, Doctor
from server.app.middleware.auth import token_required, role_required

medical_bp = Blueprint('medical_bp', __name__, url_prefix='/api/medical-records')

@medical_bp.route('', methods=['GET'])
@token_required
def list_records(current_user):
    patient_id = request.args.get('patient_id')
    query = MedicalRecord.query
    if patient_id:
        query = query.filter_by(patient_id=int(patient_id))
    elif current_user.role == 'patient' and current_user.patient_profile:
        query = query.filter_by(patient_id=current_user.patient_profile.id)

    records = query.order_by(MedicalRecord.created_at.desc()).all()
    return jsonify({'success': True, 'medical_records': [r.to_dict() for r in records]}), 200

@medical_bp.route('/<int:record_id>', methods=['GET'])
@token_required
def get_record(current_user, record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    return jsonify({'success': True, 'medical_record': record.to_dict()}), 200
