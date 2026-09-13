from flask import Blueprint, request, jsonify
from server.app.extensions import db
from server.app.models import Nurse, Patient, Vital, Notification, User
from server.app.middleware.auth import role_required
from server.app.services.patient_service import PatientService
from server.app.services.notification_service import NotificationService
from server.app.utils.validators import validate_vital_ranges
from server.app.utils.audit import log_action

nurse_bp = Blueprint('nurse_bp', __name__, url_prefix='/api/nurse')

@nurse_bp.route('/dashboard', methods=['GET'])
@role_required(['nurse', 'admin'])
def nurse_dashboard(current_user):
    nurse = current_user.nurse_profile or Nurse.query.first()
    
    patients = Patient.query.filter_by(is_active=True).all()
    recent_vitals = Vital.query.order_by(Vital.recorded_at.desc()).limit(10).all()
    abnormal_vitals = [v for v in recent_vitals if v.is_abnormal]
    
    # Active nurses on duty
    active_nurses = Nurse.query.filter_by(is_active=True).all()

    return jsonify({
        'success': True,
        'nurse': nurse.to_dict() if nurse else None,
        'stats': {
            'total_patients': len(patients),
            'vitals_recorded_today': Vital.query.count(),
            'abnormal_readings_flagged': len(abnormal_vitals),
            'current_duty_status': nurse.duty_status if nurse else 'On Duty',
            'assigned_room': nurse.assigned_room if nurse else 'General Ward'
        },
        'patients': [p.to_dict() for p in patients[:12]],
        'recent_vitals': [v.to_dict() for v in recent_vitals],
        'duty_roster': [n.to_dict() for n in active_nurses]
    }), 200

@nurse_bp.route('/vitals', methods=['POST'])
@role_required(['nurse', 'doctor', 'admin'])
def record_vitals(current_user):
    data = request.get_json() or {}
    patient_id = int(data.get('patient_id'))
    
    temp = float(data.get('temperature', 98.6))
    bp_sys = int(data.get('blood_pressure_systolic', 120))
    bp_dia = int(data.get('blood_pressure_diastolic', 80))
    hr = int(data.get('heart_rate', 72))
    spo2 = int(data.get('spo2', 98))
    weight = float(data.get('weight', 70.0))

    errors = validate_vital_ranges(temp, bp_sys, bp_dia, hr, spo2, weight)
    if errors:
        return jsonify({'success': False, 'message': ' | '.join(errors)}), 400

    vital_dict = PatientService.record_vitals(patient_id, current_user.id, data)
    patient = Patient.query.get(patient_id)

    # Check if abnormal and trigger urgent notification to doctor
    if bp_sys >= 150 or hr >= 115 or spo2 <= 92 or temp >= 101.5:
        if patient and patient.assigned_doctor:
            NotificationService.send_notification(
                user_id=patient.assigned_doctor.user_id,
                title=f"URGENT: Abnormal Vitals for {patient.user.full_name}",
                message=f"Nurse {current_user.full_name} recorded abnormal vitals: BP {bp_sys}/{bp_dia} mmHg, HR {hr} bpm, SpO2 {spo2}%.",
                type_str='Vital Warning',
                action_url=f"/doctor/patients/{patient_id}"
            )

    log_action(current_user.id, 'RECORD_VITALS', 'Vital', vital_dict['id'], f"Recorded vitals for patient #{patient_id}")
    return jsonify({
        'success': True,
        'message': 'Vital signs recorded successfully',
        'vital': vital_dict
    }), 201

@nurse_bp.route('/update-duty', methods=['PATCH'])
@role_required(['nurse', 'admin'])
def update_duty_status(current_user):
    data = request.get_json() or {}
    nurse = current_user.nurse_profile
    if not nurse:
        return jsonify({'success': False, 'message': 'Nurse profile not found'}), 404

    if 'duty_status' in data:
        nurse.duty_status = data['duty_status']
    if 'assigned_room' in data:
        nurse.assigned_room = data['assigned_room']
    if 'shift_timing' in data:
        nurse.shift_timing = data['shift_timing']

    db.session.commit()
    log_action(current_user.id, 'UPDATE_DUTY', 'Nurse', nurse.id, f"Nurse duty updated: {nurse.duty_status}, Room: {nurse.assigned_room}")
    return jsonify({
        'success': True,
        'message': 'Duty and room assignment updated',
        'nurse': nurse.to_dict()
    }), 200
