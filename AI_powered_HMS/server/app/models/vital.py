from datetime import datetime
from server.app.extensions import db

class Vital(db.Model):
    __tablename__ = 'vitals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False, index=True)
    recorded_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    
    # Clinical vitals
    temperature = db.Column(db.Float, nullable=False) # e.g. 98.6 Fahrenheit
    blood_pressure_systolic = db.Column(db.Integer, nullable=False) # e.g. 120
    blood_pressure_diastolic = db.Column(db.Integer, nullable=False) # e.g. 80
    heart_rate = db.Column(db.Integer, nullable=False) # e.g. 72 bpm
    respiratory_rate = db.Column(db.Integer, default=16) # breaths per min
    spo2 = db.Column(db.Integer, nullable=False) # e.g. 98%
    weight = db.Column(db.Float, nullable=False) # e.g. 70.5 kg
    height = db.Column(db.Float, nullable=True) # e.g. 175 cm
    bmi = db.Column(db.Float, nullable=True)
    blood_glucose = db.Column(db.Float, nullable=True) # e.g. 95 mg/dL
    notes = db.Column(db.Text, nullable=True)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    recorded_by_user = db.relationship('User', foreign_keys=[recorded_by_user_id])

    @property
    def bp_display(self):
        return f"{self.blood_pressure_systolic}/{self.blood_pressure_diastolic} mmHg"

    @property
    def is_abnormal(self):
        return (
            self.blood_pressure_systolic > 140 or
            self.blood_pressure_diastolic > 90 or
            self.heart_rate > 100 or self.heart_rate < 55 or
            self.spo2 < 95 or
            self.temperature > 100.4
        )

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'recorded_by_user_id': self.recorded_by_user_id,
            'recorded_by_name': self.recorded_by_user.full_name if self.recorded_by_user else 'Medical Staff',
            'temperature': self.temperature,
            'blood_pressure_systolic': self.blood_pressure_systolic,
            'blood_pressure_diastolic': self.blood_pressure_diastolic,
            'bp_display': self.bp_display,
            'heart_rate': self.heart_rate,
            'respiratory_rate': self.respiratory_rate,
            'spo2': self.spo2,
            'weight': self.weight,
            'height': self.height,
            'bmi': self.bmi,
            'blood_glucose': self.blood_glucose,
            'notes': self.notes,
            'is_abnormal': self.is_abnormal,
            'recorded_at': self.recorded_at.isoformat() if self.recorded_at else None
        }
