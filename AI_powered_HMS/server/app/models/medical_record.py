from datetime import datetime
from server.app.extensions import db

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id', ondelete='SET NULL'), nullable=True)
    
    diagnosis = db.Column(db.String(255), nullable=False)
    symptoms = db.Column(db.Text, nullable=True)
    treatment_plan = db.Column(db.Text, nullable=True)
    prescription = db.Column(db.Text, nullable=True)
    lab_tests_ordered = db.Column(db.Text, nullable=True)
    follow_up_date = db.Column(db.Date, nullable=True)
    attachments_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.user.full_name if self.patient and self.patient.user else 'Unknown',
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.user.full_name if self.doctor and self.doctor.user else 'Doctor',
            'specialization': self.doctor.specialization if self.doctor else '',
            'appointment_id': self.appointment_id,
            'diagnosis': self.diagnosis,
            'symptoms': self.symptoms,
            'treatment_plan': self.treatment_plan,
            'prescription': self.prescription,
            'lab_tests_ordered': self.lab_tests_ordered,
            'follow_up_date': self.follow_up_date.isoformat() if self.follow_up_date else None,
            'attachments_url': self.attachments_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
