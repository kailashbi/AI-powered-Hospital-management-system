from datetime import datetime
from server.app.extensions import db

class Nurse(db.Model):
    __tablename__ = 'nurses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id', ondelete='RESTRICT'), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    qualification = db.Column(db.String(100), nullable=True)
    shift_timing = db.Column(db.String(50), default='Morning (06:00 - 14:00)', nullable=False)
    assigned_room = db.Column(db.String(50), default='Ward A - Room 102')
    duty_status = db.Column(db.String(30), default='On Duty', nullable=False) # 'On Duty', 'Break', 'Off Duty', 'Emergency Dispatch'
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.user.full_name if self.user else 'Unknown Nurse',
            'email': self.user.email if self.user else '',
            'phone': self.user.phone if self.user else '',
            'avatar_url': self.user.avatar_url if self.user else '',
            'department_id': self.department_id,
            'department_name': self.department.name if self.department else 'General',
            'license_number': self.license_number,
            'qualification': self.qualification,
            'shift_timing': self.shift_timing,
            'assigned_room': self.assigned_room,
            'duty_status': self.duty_status,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
