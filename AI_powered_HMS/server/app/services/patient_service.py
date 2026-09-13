from datetime import datetime
from server.app.extensions import db
from server.app.models.patient import Patient
from server.app.models.vital import Vital
from server.app.models.medical_record import MedicalRecord

class PatientService:
    @staticmethod
    def get_all_patients(search_query=None):
        query = Patient.query.filter_by(is_active=True)
        if search_query:
            search_clean = f"%{search_query.strip()}%"
            query = query.join(Patient.user).filter(
                (Patient.patient_code.ilike(search_clean)) |
                (Patient.user.has(first_name=search_clean)) |
                (Patient.user.has(last_name=search_clean))
            )
        patients = query.order_by(Patient.created_at.desc()).all()
        return [p.to_dict() for p in patients]

    @staticmethod
    def get_patient_profile(patient_id: int):
        patient = Patient.query.get(patient_id)
        if not patient:
            return None
        data = patient.to_dict()
        data['vitals_history'] = [v.to_dict() for v in patient.vitals.limit(20).all()]
        data['medical_history'] = [m.to_dict() for m in patient.medical_records.limit(20).all()]
        data['predictions_history'] = [p.to_dict() for p in patient.predictions.limit(20).all()]
        return data

    @staticmethod
    def record_vitals(patient_id: int, user_id: int, vital_data: dict):
        height = vital_data.get('height')
        weight = vital_data.get('weight', 70.0)
        bmi = None
        if height and weight and height > 0:
            height_m = height / 100.0
            bmi = round(weight / (height_m * height_m), 1)

        vital = Vital(
            patient_id=patient_id,
            recorded_by_user_id=user_id,
            temperature=float(vital_data.get('temperature', 98.6)),
            blood_pressure_systolic=int(vital_data.get('blood_pressure_systolic', 120)),
            blood_pressure_diastolic=int(vital_data.get('blood_pressure_diastolic', 80)),
            heart_rate=int(vital_data.get('heart_rate', 72)),
            respiratory_rate=int(vital_data.get('respiratory_rate', 16)),
            spo2=int(vital_data.get('spo2', 98)),
            weight=float(weight),
            height=float(height) if height else None,
            bmi=bmi,
            blood_glucose=float(vital_data.get('blood_glucose')) if vital_data.get('blood_glucose') else None,
            notes=vital_data.get('notes')
        )
        db.session.add(vital)
        db.session.commit()

        # Stream Kafka Vitals Telemetry Event
        try:
            from server.app.services.kafka_service import kafka_service
            kafka_service.publish_event(
                topic=kafka_service.TOPICS['VITALS_STREAM'],
                event_type='VITAL_RECORDED',
                payload=vital.to_dict(),
                key=str(patient_id)
            )

            # Check for physiological critical thresholds
            sys_bp = vital.blood_pressure_systolic
            dia_bp = vital.blood_pressure_diastolic
            hr = vital.heart_rate
            spo2 = vital.spo2
            temp = vital.temperature

            if (sys_bp >= 160 or dia_bp >= 100 or hr >= 120 or spo2 <= 90 or temp >= 103.0):
                triggers = []
                if sys_bp >= 160 or dia_bp >= 100:
                    triggers.append(f"Severe Hypertension ({sys_bp}/{dia_bp} mmHg)")
                if hr >= 120:
                    triggers.append(f"Tachycardia ({hr} bpm)")
                if spo2 <= 90:
                    triggers.append(f"Hypoxia (SpO2 {spo2}%)")
                if temp >= 103.0:
                    triggers.append(f"High Fever ({temp}°F)")

                kafka_service.publish_event(
                    topic=kafka_service.TOPICS['EMERGENCY_ALERTS'],
                    event_type='CRITICAL_VITALS_ALERT',
                    payload={
                        'patient_id': patient_id,
                        'vital_id': vital.id,
                        'urgency': 'CRITICAL',
                        'triggers': triggers,
                        'vital_metrics': vital.to_dict()
                    },
                    key=str(patient_id)
                )
        except Exception as e:
            print(f"[Kafka Event Warning] Failed to publish vitals event: {e}")

        return vital.to_dict()

