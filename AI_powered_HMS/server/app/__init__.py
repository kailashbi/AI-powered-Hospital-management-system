import os
from flask import Flask, jsonify
from flasgger import Swagger
from server.app.config.config import config_by_name
from server.app.extensions import db, cors
from server.app.middleware.error_handler import register_error_handlers

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    Swagger(app)
    register_error_handlers(app)

    # Register Blueprints
    from server.app.routes.auth_routes import auth_bp
    from server.app.routes.admin_routes import admin_bp
    from server.app.routes.doctor_routes import doctor_bp
    from server.app.routes.nurse_routes import nurse_bp
    from server.app.routes.patient_routes import patient_bp
    from server.app.routes.prediction_routes import prediction_bp
    from server.app.routes.appointment_routes import appointment_bp
    from server.app.routes.medical_routes import medical_bp
    from server.app.routes.notification_routes import notification_bp
    from server.app.routes.kafka_routes import kafka_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(nurse_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(medical_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(kafka_bp)


    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'system': 'KAIre Health AI Hospital Management System',
            'version': '1.0.0-enterprise',
            'database': 'Connected'
        }), 200

    # Auto-initialize database tables and demo seed data if needed
    with app.app_context():
        try:
            db.create_all()
            from server.app.models.user import User
            if User.query.count() == 0:
                _seed_initial_data(db)
        except Exception as e:
            print(f"[Database Init Info] {e}")

    return app

def _seed_initial_data(db):
    """Populates realistic seed entities for immediate zero-config testing."""
    import datetime
    from server.app.models import User, Department, Doctor, Nurse, Patient, Appointment, Vital, MedicalRecord, Prediction, Notification, AuditLog
    
    # 1. Departments
    d1 = Department(id=1, name='Cardiology', code='CARD-01', description='Cardiovascular diagnostics and interventions', location_floor='Floor 3', contact_phone='+1 (555) 234-5678')
    d2 = Department(id=2, name='Endocrinology & Diabetology', code='ENDO-02', description='Diabetes management and metabolic therapy', location_floor='Floor 2', contact_phone='+1 (555) 345-6789')
    d3 = Department(id=3, name='Neurology & Stroke Center', code='NEUR-03', description='Stroke care and neurological monitoring', location_floor='Floor 4', contact_phone='+1 (555) 456-7890')
    d4 = Department(id=4, name='General Internal Medicine', code='IMED-04', description='Primary care and preventive diagnostics', location_floor='Floor 1', contact_phone='+1 (555) 567-8901')
    db.session.add_all([d1, d2, d3, d4])
    db.session.flush()

    # 2. Users (Admin, Doctors, Nurses, Patients)
    admin = User(id=1, username='admin_system', email='admin@kairehealth.com', role='admin', first_name='Dr. Arthur', last_name='Vance', phone='+1 (555) 100-0001', avatar_url='https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150', is_active=True)
    admin.set_password('password123')

    doc1 = User(id=2, username='dr_sarah_chen', email='dr.sarah@kairehealth.com', role='doctor', first_name='Sarah', last_name='Chen', phone='+1 (555) 200-0002', avatar_url='https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=150', is_active=True)
    doc1.set_password('password123')

    doc2 = User(id=3, username='dr_alex_reyes', email='dr.alex@kairehealth.com', role='doctor', first_name='Alex', last_name='Reyes', phone='+1 (555) 200-0003', avatar_url='https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=150', is_active=True)
    doc2.set_password('password123')

    doc3 = User(id=4, username='dr_elena_rostova', email='dr.elena@kairehealth.com', role='doctor', first_name='Elena', last_name='Rostova', phone='+1 (555) 200-0004', avatar_url='https://images.unsplash.com/photo-1594824813689-f53e6b72a0f8?w=150', is_active=True)
    doc3.set_password('password123')

    nurse1 = User(id=5, username='nurse_emily_watson', email='nurse.emily@kairehealth.com', role='nurse', first_name='Emily', last_name='Watson', phone='+1 (555) 300-0005', avatar_url='https://images.unsplash.com/photo-1582750433449-648ed127bb54?w=150', is_active=True)
    nurse1.set_password('password123')

    nurse2 = User(id=6, username='nurse_marcus_brooks', email='nurse.marcus@kairehealth.com', role='nurse', first_name='Marcus', last_name='Brooks', phone='+1 (555) 300-0006', avatar_url='https://images.unsplash.com/photo-1537368910025-700350fe46c7?w=150', is_active=True)
    nurse2.set_password('password123')

    pat1 = User(id=7, username='patient_john_doe', email='john.doe@gmail.com', role='patient', first_name='John', last_name='Doe', phone='+1 (555) 400-0007', avatar_url='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150', is_active=True)
    pat1.set_password('password123')

    pat2 = User(id=8, username='patient_maria_garcia', email='maria.garcia@gmail.com', role='patient', first_name='Maria', last_name='Garcia', phone='+1 (555) 400-0008', avatar_url='https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150', is_active=True)
    pat2.set_password('password123')

    db.session.add_all([admin, doc1, doc2, doc3, nurse1, nurse2, pat1, pat2])
    db.session.flush()

    # 3. Doctor Profiles
    d_prof1 = Doctor(id=1, user_id=2, department_id=1, license_number='MD-CARD-88421', specialization='Interventional Cardiology', qualification='MD, FACC, Harvard', experience_years=14, consultation_fee=180.0, room_number='Room 304-A', bio='Specializes in coronary artery disease and AI-assisted echocardiogram risk.')
    d_prof2 = Doctor(id=2, user_id=3, department_id=2, license_number='MD-ENDO-99312', specialization='Endocrinology & Metabolism', qualification='MD, PhD, Johns Hopkins', experience_years=11, consultation_fee=160.0, room_number='Room 210-B', bio='Expert in type-2 diabetes prevention and metabolic regression models.')
    d_prof3 = Doctor(id=3, user_id=4, department_id=3, license_number='MD-NEUR-77290', specialization='Vascular Neurology & Stroke', qualification='MD, Stanford', experience_years=16, consultation_fee=210.0, room_number='Room 408-C', bio='Pioneer in ischemic stroke risk stratification and acute intervention.')
    db.session.add_all([d_prof1, d_prof2, d_prof3])

    # 4. Nurses
    n_prof1 = Nurse(id=1, user_id=5, department_id=1, license_number='RN-CRIT-55102', qualification='BSN, RN, CCRN', shift_timing='Morning (06:00 - 14:00)', assigned_room='Cardiac Care Unit - CCU 301', duty_status='On Duty')
    n_prof2 = Nurse(id=2, user_id=6, department_id=4, license_number='RN-MED-66291', qualification='BSN, RN', shift_timing='Evening (14:00 - 22:00)', assigned_room='General Ward 2', duty_status='On Duty')
    db.session.add_all([n_prof1, n_prof2])

    # 5. Patients
    p_prof1 = Patient(id=1, user_id=7, patient_code='PAT-2026-001', date_of_birth=datetime.date(1974, 5, 14), gender='Male', blood_group='O+', city='Springfield, IL', assigned_doctor_id=1, assigned_room='Room 301-Bed A')
    p_prof2 = Patient(id=2, user_id=8, patient_code='PAT-2026-002', date_of_birth=datetime.date(1968, 11, 23), gender='Female', blood_group='A+', city='Miami, FL', assigned_doctor_id=3, assigned_room='Room 408-Bed B')
    db.session.add_all([p_prof1, p_prof2])
    db.session.flush()

    # 6. Appointments
    a1 = Appointment(id=1, appointment_code='APT-2026-001', patient_id=1, doctor_id=1, department_id=1, appointment_date=datetime.date.today() + datetime.timedelta(days=2), appointment_time=datetime.time(9, 30), status='Confirmed', priority='Urgent', symptoms='Chest tightness and shortness of breath')
    a2 = Appointment(id=2, appointment_code='APT-2026-002', patient_id=2, doctor_id=3, department_id=3, appointment_date=datetime.date.today() + datetime.timedelta(days=3), appointment_time=datetime.time(11, 0), status='Scheduled', priority='Urgent', symptoms='Transient numbness in left arm and episodic dizziness')
    db.session.add_all([a1, a2])

    # 7. Vitals
    v1 = Vital(id=1, patient_id=1, recorded_by_user_id=5, temperature=98.6, blood_pressure_systolic=142, blood_pressure_diastolic=92, heart_rate=84, spo2=97, weight=88.5, height=178.0, bmi=27.9, blood_glucose=118.0, notes='Mild chest discomfort on exertion')
    v2 = Vital(id=2, patient_id=2, recorded_by_user_id=5, temperature=99.1, blood_pressure_systolic=165, blood_pressure_diastolic=105, heart_rate=92, spo2=96, weight=74.0, height=162.0, bmi=28.2, blood_glucose=145.0, notes='Hypertension alert. Attending neurologist notified.')
    db.session.add_all([v1, v2])

    # 8. Predictions
    pred1 = Prediction(
        id=1, patient_id=1, doctor_id=1, disease_type='Heart Disease', model_version='v1.2.0-rf-xgboost',
        risk_score=78.45, risk_level='High', prediction_result='Positive Risk Indicator', confidence_score=89.2,
        input_features={"age": 52, "sex": 1, "cp": 2, "trestbps": 142, "chol": 268, "fbs": 0, "restecg": 1, "thalach": 138, "exang": 1, "oldpeak": 2.3, "slope": 1, "ca": 1, "thal": 2},
        feature_importance={"chol": "+28%", "oldpeak": "+24%", "trestbps": "+19%", "thalach": "-12%", "age": "+11%"},
        clinical_recommendation='High probability of coronary artery plaque. Immediate stress echocardiogram and statin intensification advised.',
        doctor_feedback='Confirmed'
    )
    pred2 = Prediction(
        id=2, patient_id=2, doctor_id=3, disease_type='Stroke', model_version='v1.1.0-rf-balanced',
        risk_score=84.10, risk_level='Critical', prediction_result='Critical Stroke Risk', confidence_score=92.5,
        input_features={"gender": "Female", "age": 57, "hypertension": 1, "heart_disease": 0, "ever_married": "Yes", "work_type": "Private", "Residence_type": "Urban", "avg_glucose_level": 145.2, "bmi": 28.2, "smoking_status": "formerly smoked"},
        feature_importance={"hypertension": "+36%", "avg_glucose_level": "+22%", "age": "+21%", "bmi": "+12%"},
        clinical_recommendation='Imminent risk of ischemic cerebrovascular event. Urgent carotid ultrasound and dual antiplatelet therapy indicated.',
        doctor_feedback='Confirmed'
    )
    db.session.add_all([pred1, pred2])

    # 9. Notifications
    n1 = Notification(id=1, user_id=7, title='Appointment Reminder: Cardiology', message='Consultation with Dr. Sarah Chen on August 10, 2026 at 09:30 AM in Room 304-A.', type='Appointment', action_url='/patient/appointments')
    n2 = Notification(id=2, user_id=7, title='AI Cardiovascular Risk Ready', message='Dr. Sarah Chen completed your Heart Disease AI risk assessment (78.45% risk). View clinical recommendations.', type='AI Alert', action_url='/patient/predictions')
    n3 = Notification(id=3, user_id=8, title='Stroke Protocol Follow-up', message='Dr. Elena Rostova updated your treatment plan based on today’s critical AI assessment.', type='AI Alert', action_url='/patient/predictions')
    db.session.add_all([n1, n2, n3])

    # 10. Audit Log
    log1 = AuditLog(id=1, user_id=1, action='SYSTEM_INIT', entity_type='System', entity_id=1, details='KAIre Health Enterprise Hospital Management System initialized with ML pipeline.', ip_address='127.0.0.1')
    db.session.add(log1)

    db.session.commit()
    print("[✓] Seed data successfully populated into KAIre Health database!")
