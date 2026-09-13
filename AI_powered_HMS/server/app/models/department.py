from datetime import datetime
from server.app.extensions import db

class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    head_doctor_id = db.Column(db.Integer, nullable=True)
    location_floor = db.Column(db.String(50), nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    doctors = db.relationship('Doctor', backref='department', lazy='dynamic')
    nurses = db.relationship('Nurse', backref='department', lazy='dynamic')
    appointments = db.relationship('Appointment', backref='department', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'head_doctor_id': self.head_doctor_id,
            'location_floor': self.location_floor,
            'contact_phone': self.contact_phone,
            'doctor_count': self.doctors.count() if hasattr(self, 'doctors') else 0,
            'nurse_count': self.nurses.count() if hasattr(self, 'nurses') else 0,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
