from datetime import datetime
from server.app.extensions import db

class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    patient_code = db.Column(db.String(30), unique=True, nullable=False, index=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False) # 'Male', 'Female', 'Other'
    blood_group = db.Column(db.String(10), nullable=True) # 'O+', 'A+', 'B+', etc.
    marital_status = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    emergency_contact_name = db.Column(db.String(100), nullable=True)
    emergency_contact_phone = db.Column(db.String(20), nullable=True)
    insurance_provider = db.Column(db.String(100), nullable=True)
    insurance_policy_number = db.Column(db.String(50), nullable=True)
    allergies = db.Column(db.Text, nullable=True)
    assigned_doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='SET NULL'), nullable=True)
    assigned_room = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    appointments = db.relationship('Appointment', backref='patient', lazy='dynamic', cascade="all, delete-orphan")
    vitals = db.relationship('Vital', backref='patient', lazy='dynamic', cascade="all, delete-orphan", order_by="desc(Vital.recorded_at)")
    medical_records = db.relationship('MedicalRecord', backref='patient', lazy='dynamic', cascade="all, delete-orphan", order_by="desc(MedicalRecord.created_at)")
    predictions = db.relationship('Prediction', backref='patient', lazy='dynamic', cascade="all, delete-orphan", order_by="desc(Prediction.created_at)")

    @property
    def age(self):
        if not self.date_of_birth:
            return 0
        today = datetime.utcnow().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def to_dict(self):
        latest_vital = self.vitals.first()
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.user.full_name if self.user else 'Unknown Patient',
            'email': self.user.email if self.user else '',
            'phone': self.user.phone if self.user else '',
            'avatar_url': self.user.avatar_url if self.user else '',
            'patient_code': self.patient_code,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'age': self.age,
            'gender': self.gender,
            'blood_group': self.blood_group,
            'marital_status': self.marital_status,
            'address': self.address,
            'city': self.city,
            'emergency_contact_name': self.emergency_contact_name,
            'emergency_contact_phone': self.emergency_contact_phone,
            'insurance_provider': self.insurance_provider,
            'insurance_policy_number': self.insurance_policy_number,
            'allergies': self.allergies,
            'assigned_doctor_id': self.assigned_doctor_id,
            'assigned_doctor_name': self.assigned_doctor.user.full_name if self.assigned_doctor and self.assigned_doctor.user else None,
            'assigned_room': self.assigned_room,
            'latest_vital': latest_vital.to_dict() if latest_vital else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
