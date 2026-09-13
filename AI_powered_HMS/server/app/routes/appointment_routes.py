from flask import Blueprint, request, jsonify
from server.app.extensions import db
from server.app.models import Appointment, Doctor, Patient, Department
from server.app.middleware.auth import token_required, role_required
from server.app.services.appointment_service import AppointmentService
from server.app.services.notification_service import NotificationService

appointment_bp = Blueprint('appointment_bp', __name__, url_prefix='/api/appointments')

@appointment_bp.route('', methods=['GET'])
@token_required
def list_appointments(current_user):
    status_filter = request.args.get('status')
    query = Appointment.query
    if current_user.role == 'doctor' and current_user.doctor_profile:
        query = query.filter_by(doctor_id=current_user.doctor_profile.id)
    elif current_user.role == 'patient' and current_user.patient_profile:
        query = query.filter_by(patient_id=current_user.patient_profile.id)

    if status_filter:
        query = query.filter_by(status=status_filter)

    appts = query.order_by(Appointment.appointment_date.desc()).all()
    return jsonify({'success': True, 'appointments': [a.to_dict() for a in appts]}), 200

@appointment_bp.route('', methods=['POST'])
@token_required
def create_appointment(current_user):
    data = request.get_json() or {}
    patient_id = data.get('patient_id')
    if current_user.role == 'patient' and current_user.patient_profile:
        patient_id = current_user.patient_profile.id

    doctor_id = int(data['doctor_id'])
    department_id = int(data.get('department_id', 1))
    date_str = data['appointment_date']
    time_str = data['appointment_time']
    symptoms = data.get('symptoms')
    priority = data.get('priority', 'Normal')

    appt = AppointmentService.create_appointment(
        patient_id, doctor_id, department_id, date_str, time_str, symptoms, priority
    )
    return jsonify({'success': True, 'appointment': appt}), 201

@appointment_bp.route('/<int:appt_id>/status', methods=['PATCH'])
@role_required(['doctor', 'admin', 'nurse'])
def update_status(current_user, appt_id):
    data = request.get_json() or {}
    status = data.get('status', 'Confirmed')
    notes = data.get('doctor_notes')
    appt = AppointmentService.update_status(appt_id, status, notes)
    if not appt:
        return jsonify({'success': False, 'message': 'Appointment not found'}), 404
    return jsonify({'success': True, 'appointment': appt}), 200

@appointment_bp.route('/<int:appt_id>/remind', methods=['POST'])
@role_required(['doctor', 'nurse', 'admin'])
def send_reminder(current_user, appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    notif = NotificationService.send_notification(
        user_id=appt.patient.user_id,
        title="Upcoming Appointment Alert",
        message=f"Reminder: You have an appointment with Dr. {appt.doctor.user.last_name} on {appt.appointment_date} at {appt.appointment_time}. Please arrive 10 minutes early.",
        type_str='Appointment',
        action_url='/patient/appointments'
    )
    return jsonify({'success': True, 'message': 'Appointment reminder notification sent to patient', 'notification': notif}), 200
