import os
import sys
from server.app.extensions import db
from server.app.models.prediction import Prediction
from server.app.models.patient import Patient
from server.app.models.notification import Notification

# Ensure ML package is reachable
try:
    from ml.inference.predictor import predictor_engine
except ImportError:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    sys.path.append(base_dir)
    from ml.inference.predictor import predictor_engine

class PredictionService:
    @staticmethod
    def run_prediction(patient_id: int, doctor_id: int, disease_type: str, features: dict):
        patient = Patient.query.get(patient_id)
        if not patient:
            raise ValueError(f"Patient with ID {patient_id} not found.")

        disease_clean = disease_type.strip().lower()

        if 'heart' in disease_clean:
            result = predictor_engine.predict_heart(features)
        elif 'diab' in disease_clean:
            result = predictor_engine.predict_diabetes(features)
        elif 'stroke' in disease_clean:
            result = predictor_engine.predict_stroke(features)
        else:
            raise ValueError(f"Unsupported disease type: {disease_type}. Valid: Heart Disease, Diabetes, Stroke")

        prediction_rec = Prediction(
            patient_id=patient_id,
            doctor_id=doctor_id,
            disease_type=result['disease_type'],
            model_version=result['model_version'],
            risk_score=result['risk_score'],
            risk_level=result['risk_level'],
            prediction_result=result['prediction_result'],
            confidence_score=result['confidence_score'],
            input_features=result['input_features'],
            feature_importance=result['feature_importance'],
            clinical_recommendation=result['clinical_recommendation'],
            doctor_feedback='Confirmed' if result['risk_level'] in ['High', 'Critical'] else 'Pending Review'
        )

        db.session.add(prediction_rec)
        db.session.commit()

        # Stream Kafka AI Prediction Event
        try:
            from server.app.services.kafka_service import kafka_service
            kafka_service.publish_event(
                topic=kafka_service.TOPICS['ML_PREDICTIONS'],
                event_type='PREDICTION_COMPLETED',
                payload=prediction_rec.to_dict(),
                key=str(patient_id)
            )
        except Exception as e:
            print(f"[Kafka Event Warning] Failed to publish prediction event: {e}")

        # If risk is elevated, dispatch automated alert to patient
        if result['risk_level'] in ['Moderate', 'High', 'Critical']:
            notif = Notification(
                user_id=patient.user_id,
                title=f"AI Health Diagnostic: {result['disease_type']} Alert",
                message=f"A new {result['disease_type']} assessment ({result['risk_level']} Risk - {result['risk_score']}%) has been evaluated by your physician. Please check recommendations.",
                type='AI Alert',
                action_url='/patient/predictions'
            )
            db.session.add(notif)
            db.session.commit()

        return prediction_rec.to_dict()


    @staticmethod
    def get_patient_history(patient_id: int):
        records = Prediction.query.filter_by(patient_id=patient_id).order_by(Prediction.created_at.desc()).all()
        return [r.to_dict() for r in records]

    @staticmethod
    def get_doctor_predictions(doctor_id: int):
        records = Prediction.query.filter_by(doctor_id=doctor_id).order_by(Prediction.created_at.desc()).all()
        return [r.to_dict() for r in records]
