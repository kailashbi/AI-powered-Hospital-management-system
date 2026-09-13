from datetime import datetime
from server.app.extensions import db

class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id', ondelete='RESTRICT'), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100), nullable=True)
    experience_years = db.Column(db.Integer, default=0)
    consultation_fee = db.Column(db.Float, default=0.0)
    room_number = db.Column(db.String(20), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    available_days = db.Column(db.String(100), default='Mon,Tue,Wed,Thu,Fri')
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    appointments = db.relationship('Appointment', backref='doctor', lazy='dynamic', cascade="all, delete-orphan")
    medical_records = db.relationship('MedicalRecord', backref='doctor', lazy='dynamic', cascade="all, delete-orphan")
    predictions = db.relationship('Prediction', backref='doctor', lazy='dynamic', cascade="all, delete-orphan")
    assigned_patients = db.relationship('Patient', backref='assigned_doctor', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.user.full_name if self.user else 'Unknown Doctor',
            'email': self.user.email if self.user else '',
            'phone': self.user.phone if self.user else '',
            'avatar_url': self.user.avatar_url if self.user else '',
            'department_id': self.department_id,
            'department_name': self.department.name if self.department else 'General',
            'license_number': self.license_number,
            'specialization': self.specialization,
            'qualification': self.qualification,
            'experience_years': self.experience_years,
            'consultation_fee': self.consultation_fee,
            'room_number': self.room_number,
            'bio': self.bio,
            'available_days': self.available_days,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
