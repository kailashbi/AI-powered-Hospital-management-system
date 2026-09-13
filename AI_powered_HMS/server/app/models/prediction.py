import json
from datetime import datetime
from server.app.extensions import db

class Prediction(db.Model):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), nullable=False)
    disease_type = db.Column(db.String(50), nullable=False, index=True) # 'Heart Disease', 'Diabetes', 'Stroke'
    model_version = db.Column(db.String(50), default='v1.0.0-xgb', nullable=False)
    risk_score = db.Column(db.Float, nullable=False) # e.g. 78.45 (%)
    risk_level = db.Column(db.String(30), nullable=False) # 'Low', 'Moderate', 'High', 'Critical'
    prediction_result = db.Column(db.String(100), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    input_features = db.Column(db.JSON, nullable=False)
    feature_importance = db.Column(db.JSON, nullable=True)
    clinical_recommendation = db.Column(db.Text, nullable=True)
    doctor_feedback = db.Column(db.String(50), default='Pending Review') # 'Pending Review', 'Confirmed', 'False Positive'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.user.full_name if self.patient and self.patient.user else 'Unknown',
            'patient_code': self.patient.patient_code if self.patient else '',
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.user.full_name if self.doctor and self.doctor.user else 'Doctor',
            'disease_type': self.disease_type,
            'model_version': self.model_version,
            'risk_score': self.risk_score,
            'risk_level': self.risk_level,
            'prediction_result': self.prediction_result,
            'confidence_score': self.confidence_score,
            'input_features': self.input_features if isinstance(self.input_features, dict) else (json.loads(self.input_features) if self.input_features else {}),
            'feature_importance': self.feature_importance if isinstance(self.feature_importance, dict) else (json.loads(self.feature_importance) if self.feature_importance else {}),
            'clinical_recommendation': self.clinical_recommendation,
            'doctor_feedback': self.doctor_feedback,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
