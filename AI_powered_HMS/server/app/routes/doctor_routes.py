from flask import Blueprint, request, jsonify
from server.app.extensions import db
from server.app.models import Doctor, Patient, Appointment, MedicalRecord, Vital, Prediction, Notification
from server.app.middleware.auth import role_required
from server.app.services.prediction_service import PredictionService
from server.app.services.notification_service import NotificationService
from server.app.utils.audit import log_action

doctor_bp = Blueprint('doctor_bp', __name__, url_prefix='/api/doctor')

@doctor_bp.route('/dashboard', methods=['GET'])
@role_required(['doctor', 'admin'])
def doctor_dashboard(current_user):
    doctor = current_user.doctor_profile or Doctor.query.first()
    if not doctor:
        return jsonify({'success': False, 'message': 'Doctor profile not associated'}), 404

    # Assigned or department patients
    patients = Patient.query.filter_by(is_active=True).all()
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).order_by(Appointment.appointment_date.asc()).limit(10).all()
    recent_predictions = Prediction.query.filter_by(doctor_id=doctor.id).order_by(Prediction.created_at.desc()).limit(8).all()
    critical_alerts = Prediction.query.filter(Prediction.risk_level.in_(['High', 'Critical'])).order_by(Prediction.created_at.desc()).limit(5).all()

    return jsonify({
        'success': True,
        'doctor': doctor.to_dict(),
        'stats': {
            'total_patients': len(patients),
            'upcoming_appointments': len([a for a in appointments if a.status in ['Scheduled', 'Confirmed']]),
            'total_predictions_run': Prediction.query.filter_by(doctor_id=doctor.id).count(),
            'critical_cases': len(critical_alerts)
        },
        'appointments': [a.to_dict() for a in appointments],
        'recent_predictions': [p.to_dict() for p in recent_predictions],
        'critical_alerts': [p.to_dict() for p in critical_alerts]
    }), 200

@doctor_bp.route('/patients', methods=['GET'])
@role_required(['doctor', 'admin'])
def get_patients(current_user):
    search = request.args.get('search')
    query = Patient.query.filter_by(is_active=True)
    if search:
        search_fmt = f"%{search.strip()}%"
        query = query.filter(
            (Patient.patient_code.ilike(search_fmt)) |
            (Patient.city.ilike(search_fmt))
        )
    patients = query.order_by(Patient.created_at.desc()).all()
    return jsonify({'success': True, 'patients': [p.to_dict() for p in patients]}), 200

@doctor_bp.route('/patients/<int:patient_id>', methods=['GET'])
@role_required(['doctor', 'nurse', 'admin'])
def get_patient_detail(current_user, patient_id):
    patient = Patient.query.get_or_404(patient_id)
    profile = patient.to_dict()
    profile['vitals'] = [v.to_dict() for v in patient.vitals.order_by(Vital.recorded_at.desc()).all()]
    profile['medical_records'] = [m.to_dict() for m in patient.medical_records.order_by(MedicalRecord.created_at.desc()).all()]
    profile['predictions'] = [p.to_dict() for p in patient.predictions.order_by(Prediction.created_at.desc()).all()]
    profile['appointments'] = [a.to_dict() for a in patient.appointments.order_by(Appointment.appointment_date.desc()).all()]
    return jsonify({'success': True, 'patient': profile}), 200

@doctor_bp.route('/medical-records', methods=['POST'])
@role_required(['doctor', 'admin'])
def create_medical_record(current_user):
    data = request.get_json() or {}
    doctor = current_user.doctor_profile or Doctor.query.first()
    
    record = MedicalRecord(
        patient_id=int(data['patient_id']),
        doctor_id=doctor.id,
        appointment_id=data.get('appointment_id'),
        diagnosis=data['diagnosis'],
        symptoms=data.get('symptoms'),
        treatment_plan=data.get('treatment_plan'),
        prescription=data.get('prescription'),
        lab_tests_ordered=data.get('lab_tests_ordered'),
        follow_up_date=data.get('follow_up_date')
    )
    db.session.add(record)
    db.session.commit()

    patient = Patient.query.get(record.patient_id)
    if patient:
        NotificationService.send_notification(
            user_id=patient.user_id,
            title="New Medical Record Added",
            message=f"Dr. {current_user.last_name} has documented your diagnosis: {record.diagnosis}.",
            type_str="General",
            action_url="/patient/medical-records"
        )

    log_action(current_user.id, 'CREATE_MEDICAL_RECORD', 'MedicalRecord', record.id, f"Added EHR diagnosis for patient ID {record.patient_id}")
    return jsonify({'success': True, 'medical_record': record.to_dict()}), 201

@doctor_bp.route('/send-patient-notification', methods=['POST'])
@role_required(['doctor', 'admin'])
def send_patient_alert(current_user):
    """
    Sends personalized appointment reminders or clinical recommendations to a patient
    """
    data = request.get_json() or {}
    patient_id = int(data.get('patient_id'))
    title = data.get('title', 'Appointment Reminder & Clinical Instructions')
    message = data.get('message', '')

    patient = Patient.query.get_or_404(patient_id)
    notif = NotificationService.send_notification(
        user_id=patient.user_id,
        title=title,
        message=message,
        type_str=data.get('type', 'Appointment'),
        action_url='/patient/appointments'
    )
    log_action(current_user.id, 'NOTIFY_PATIENT', 'Notification', notif['id'], f"Doctor sent reminder to Patient #{patient.patient_code}")
    return jsonify({'success': True, 'message': 'Notification dispatched to patient successfully', 'notification': notif}), 200
