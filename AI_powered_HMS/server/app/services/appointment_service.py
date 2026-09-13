import uuid
from datetime import datetime
from server.app.extensions import db
from server.app.models.appointment import Appointment
from server.app.models.patient import Patient
from server.app.models.doctor import Doctor
from server.app.models.notification import Notification

class AppointmentService:
    @staticmethod
    def create_appointment(patient_id, doctor_id, department_id, date_str, time_str, symptoms=None, priority='Normal'):
        doctor = Doctor.query.get(doctor_id)
        patient = Patient.query.get(patient_id)
        if not doctor or not patient:
            raise ValueError("Doctor or Patient not found")

        code = f"APT-{datetime.utcnow().year}-{str(uuid.uuid4())[:6].upper()}"
        appt_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        appt_time = datetime.strptime(time_str, '%H:%M').time() if len(time_str) == 5 else datetime.strptime(time_str, '%H:%M:%S').time()

        appointment = Appointment(
            appointment_code=code,
            patient_id=patient_id,
            doctor_id=doctor_id,
            department_id=department_id,
            appointment_date=appt_date,
            appointment_time=appt_time,
            status='Confirmed',
            priority=priority,
            symptoms=symptoms
        )
        db.session.add(appointment)
        db.session.commit()

        # Send notification to Patient
        notif_patient = Notification(
            user_id=patient.user_id,
            title="Appointment Confirmed",
            message=f"Your appointment with Dr. {doctor.user.last_name} is scheduled for {date_str} at {time_str}.",
            type='Appointment',
            action_url='/patient/appointments'
        )
        # Send notification to Doctor
        notif_doc = Notification(
            user_id=doctor.user_id,
            title="New Patient Booking",
            message=f"Patient {patient.user.full_name} booked a {priority} consultation for {date_str} at {time_str}.",
            type='Appointment',
            action_url='/doctor/appointments'
        )
        db.session.add(notif_patient)
        db.session.add(notif_doc)
        db.session.commit()

        # Stream Kafka Appointment Event
        try:
            from server.app.services.kafka_service import kafka_service
            kafka_service.publish_event(
                topic=kafka_service.TOPICS['APPOINTMENTS'],
                event_type='APPOINTMENT_CREATED',
                payload=appointment.to_dict(),
                key=str(patient_id)
            )
        except Exception as e:
            print(f"[Kafka Event Warning] Failed to publish appointment event: {e}")

        return appointment.to_dict()


    @staticmethod
    def update_status(appointment_id, status, notes=None):
        appt = Appointment.query.get(appointment_id)
        if not appt:
            return None
        appt.status = status
        if notes:
            appt.doctor_notes = notes
        db.session.commit()

        # Notify patient of status change
        notif = Notification(
            user_id=appt.patient.user_id,
            title=f"Appointment Status Update: {status}",
            message=f"Your appointment on {appt.appointment_date} with Dr. {appt.doctor.user.last_name} has been updated to {status}.",
            type='Appointment',
            action_url='/patient/appointments'
        )
        db.session.add(notif)
        db.session.commit()

        return appt.to_dict()
