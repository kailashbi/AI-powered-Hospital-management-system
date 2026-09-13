from datetime import datetime
from server.app.extensions import db

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_code = db.Column(db.String(30), unique=True, nullable=False, index=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id', ondelete='RESTRICT'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False, index=True)
    appointment_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(30), default='Scheduled', nullable=False) # 'Scheduled', 'Confirmed', 'In-Progress', 'Completed', 'Cancelled'
    priority = db.Column(db.String(20), default='Normal', nullable=False) # 'Low', 'Normal', 'Urgent', 'Emergency'
    symptoms = db.Column(db.Text, nullable=True)
    doctor_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    medical_record = db.relationship('MedicalRecord', backref='appointment', uselist=False)

    def to_dict(self):
        return {
            'id': self.id,
            'appointment_code': self.appointment_code,
            'patient_id': self.patient_id,
            'patient_name': self.patient.user.full_name if self.patient and self.patient.user else 'Unknown Patient',
            'patient_code': self.patient.patient_code if self.patient else '',
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.user.full_name if self.doctor and self.doctor.user else 'Unknown Doctor',
            'department_id': self.department_id,
            'department_name': self.department.name if self.department else 'General',
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'appointment_time': self.appointment_time.strftime('%H:%M') if self.appointment_time else None,
            'status': self.status,
            'priority': self.priority,
            'symptoms': self.symptoms,
            'doctor_notes': self.doctor_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
