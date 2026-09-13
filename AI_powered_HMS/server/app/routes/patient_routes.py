from flask import Blueprint, request, jsonify
from server.app.extensions import db
from server.app.models import Patient, Appointment, MedicalRecord, Vital, Prediction, Notification
from server.app.middleware.auth import role_required
from server.app.services.appointment_service import AppointmentService

patient_bp = Blueprint('patient_bp', __name__, url_prefix='/api/patient')

@patient_bp.route('/dashboard', methods=['GET'])
@role_required(['patient', 'admin'])
def patient_dashboard(current_user):
    patient = current_user.patient_profile or Patient.query.first()
    if not patient:
        return jsonify({'success': False, 'message': 'Patient profile not found'}), 404

    appointments = Appointment.query.filter_by(patient_id=patient.id).order_by(Appointment.appointment_date.desc()).all()
    vitals = Vital.query.filter_by(patient_id=patient.id).order_by(Vital.recorded_at.desc()).limit(15).all()
    predictions = Prediction.query.filter_by(patient_id=patient.id).order_by(Prediction.created_at.desc()).all()
    medical_records = MedicalRecord.query.filter_by(patient_id=patient.id).order_by(MedicalRecord.created_at.desc()).all()
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(10).all()

    latest_prediction = predictions[0] if predictions else None

    return jsonify({
        'success': True,
        'profile': patient.to_dict(),
        'stats': {
            'upcoming_appointments': len([a for a in appointments if a.status in ['Scheduled', 'Confirmed']]),
            'total_medical_records': len(medical_records),
            'latest_vital_bp': vitals[0].bp_display if vitals else 'N/A',
            'latest_vital_hr': vitals[0].heart_rate if vitals else 'N/A',
            'latest_ai_risk': latest_prediction.risk_score if latest_prediction else None,
            'latest_ai_disease': latest_prediction.disease_type if latest_prediction else None
        },
        'appointments': [a.to_dict() for a in appointments],
        'vitals_history': [v.to_dict() for v in vitals],
        'predictions': [p.to_dict() for p in predictions],
        'medical_records': [m.to_dict() for m in medical_records],
        'notifications': [n.to_dict() for n in notifications]
    }), 200

@patient_bp.route('/appointments', methods=['GET', 'POST'])
@role_required(['patient', 'admin'])
def handle_appointments(current_user):
    patient = current_user.patient_profile or Patient.query.first()
    if request.method == 'GET':
        appts = Appointment.query.filter_by(patient_id=patient.id).order_by(Appointment.appointment_date.desc()).all()
        return jsonify({'success': True, 'appointments': [a.to_dict() for a in appts]}), 200

    data = request.get_json() or {}
    doctor_id = int(data['doctor_id'])
    department_id = int(data.get('department_id', 1))
    date_str = data['appointment_date']
    time_str = data['appointment_time']
    symptoms = data.get('symptoms', '')
    priority = data.get('priority', 'Normal')

    appt_dict = AppointmentService.create_appointment(
        patient.id, doctor_id, department_id, date_str, time_str, symptoms, priority
    )
    return jsonify({'success': True, 'message': 'Appointment booked successfully', 'appointment': appt_dict}), 201

@patient_bp.route('/vitals', methods=['GET'])
@role_required(['patient', 'admin'])
def get_vitals(current_user):
    patient = current_user.patient_profile or Patient.query.first()
    vitals = Vital.query.filter_by(patient_id=patient.id).order_by(Vital.recorded_at.desc()).all()
    return jsonify({'success': True, 'vitals': [v.to_dict() for v in vitals]}), 200

@patient_bp.route('/medical-records', methods=['GET'])
@role_required(['patient', 'admin'])
def get_medical_records(current_user):
    patient = current_user.patient_profile or Patient.query.first()
    records = MedicalRecord.query.filter_by(patient_id=patient.id).order_by(MedicalRecord.created_at.desc()).all()
    return jsonify({'success': True, 'medical_records': [m.to_dict() for m in records]}), 200

@patient_bp.route('/predictions', methods=['GET'])
@role_required(['patient', 'admin'])
def get_predictions(current_user):
    patient = current_user.patient_profile or Patient.query.first()
    preds = Prediction.query.filter_by(patient_id=patient.id).order_by(Prediction.created_at.desc()).all()
    return jsonify({'success': True, 'predictions': [p.to_dict() for p in preds]}), 200
