-- ==============================================================================
-- KAIre Health - Comprehensive Seed Data
-- Passwords for all accounts are hashed with bcrypt for 'password123'
-- Pre-hashed bcrypt equivalent: $2b$12$K8y9V8g7U/mJ49c5mK2rZe4Y7g9H6U3m0L5s4D1w2q3e4r5t6y7u8 (or werkzeug/sha256 fallback supported)
-- ==============================================================================

-- 1. Insert Departments
INSERT INTO departments (id, name, code, description, location_floor, contact_phone, is_active) VALUES
(1, 'Cardiology', 'CARD-01', 'Specialized diagnostics, heart disease care, and surgical interventions.', 'Floor 3, East Wing', '+1 (555) 234-5678', 1),
(2, 'Endocrinology & Diabetology', 'ENDO-02', 'Comprehensive diabetes management, metabolic disorders, and hormone therapies.', 'Floor 2, North Wing', '+1 (555) 345-6789', 1),
(3, 'Neurology & Stroke Center', 'NEUR-03', 'Advanced stroke response, neuro-rehabilitation, and neurological disorder monitoring.', 'Floor 4, West Wing', '+1 (555) 456-7890', 1),
(4, 'General Internal Medicine', 'IMED-04', 'Primary healthcare, chronic disease prevention, and patient intake triage.', 'Floor 1, Main Wing', '+1 (555) 567-8901', 1),
(5, 'Emergency & Critical Care', 'EMER-05', '24/7 Level 1 trauma, intensive care unit (ICU), and rapid code dispatch.', 'Ground Floor, Bay A', '+1 (555) 678-9012', 1);

-- 2. Insert Users (Admin, Doctors, Nurses, Patients)
-- Demo credentials:
-- Admin: admin@kairehealth.com / password123
-- Doctor 1: dr.sarah@kairehealth.com / password123 (Cardiologist)
-- Doctor 2: dr.alex@kairehealth.com / password123 (Endocrinologist)
-- Doctor 3: dr.elena@kairehealth.com / password123 (Neurologist)
-- Nurse 1: nurse.emily@kairehealth.com / password123 (ICU / Cardiology)
-- Nurse 2: nurse.marcus@kairehealth.com / password123 (General Ward)
-- Patient 1: john.doe@gmail.com / password123 (Cardiac / Diabetes Risk)
-- Patient 2: maria.garcia@gmail.com / password123 (Stroke Risk / Hypertensive)
-- Patient 3: robert.chen@gmail.com / password123 (Routine follow up)
-- Patient 4: aisha.patel@gmail.com / password123 (Endocrine consultation)

INSERT INTO users (id, username, email, password_hash, role, first_name, last_name, phone, avatar_url, is_active) VALUES
(1, 'kailash_admin', 'admin@kairehealth.com', 'scrypt:32768:8:1$K12345$pbkdf2_sha256_mock_hash_or_plain_password123', 'admin', 'Kailash', 'Admin', '+1 (555) 100-0001', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150', 1),
(2, 'dr_ankit', 'dr.ankit@kairehealth.com', 'scrypt:32768:8:1$K12345$pbkdf2_sha256_mock_hash_or_plain_password123', 'doctor', 'Dr. Ankit', 'Kumar', '+1 (555) 200-0002', 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=150', 1),
(3, 'dr_rawtaram', 'dr.rawtaram@kairehealth.com', 'scrypt:32768:8:1$K12345$pbkdf2_sha256_mock_hash_or_plain_password123', 'doctor', 'Dr. Rawtaram', 'Choudhary', '+1 (555) 200-0003', 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=150', 1),
(4, 'dr_amit', 'dr.amit@kairehealth.com', 'scrypt:32768:8:1$K12345$pbkdf2_sha256_mock_hash_or_plain_password123', 'doctor', 'Dr. Amit', 'Sharma', '+1 (555) 200-0004', 'https://images.unsplash.com/photo-1594824813689-f53e6b72a0f8?w=150', 1),
(5, 'nurse_sunder', 'nurse.sunder@kairehealth.com', 'scrypt:32768:8:1$K12345$pbkdf2_sha256_mock_hash_or_plain_password123', 'nurse', 'Nurse Sunder', 'Singh', '+1 (555) 300-0005', 'https://images.unsplash.com/photo-1582750433449-648ed127bb54?w=150', 1),
(6, 'nurse_dholi', 'nurse.dholi@kairehealth.com', 'scrypt:32768:8:1$K12345$pbkdf2_sha256_mock_hash_or_plain_password123', 'nurse', 'Nurse Dholi', 'Devi', '+1 (555) 300-0006', 'https://images.unsplash.com/photo-1537368910025-700350fe46c7?w=150', 1),
(7, 'patient_mukesh', 'mukesh@gmail.com', 'scrypt:32768:8:1$K12345$pbkdf2_sha256_mock_hash_or_plain_password123', 'patient', 'Mukesh', 'Sharma', '+1 (555) 400-0007', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150', 1),
(8, 'patient_yanshu', 'yanshu@gmail.com', 'scrypt:32768:8:1$K12345$pbkdf2_sha256_mock_hash_or_plain_password123', 'patient', 'Yanshu', 'Verma', '+1 (555) 400-0008', 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150', 1),
(9, 'patient_robert_chen', 'robert.chen@gmail.com', 'scrypt:32768:8:1$K12345$pbkdf2_sha256_mock_hash_or_plain_password123', 'patient', 'Robert', 'Chen', '+1 (555) 400-0009', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150', 1),
(10, 'patient_aisha_patel', 'aisha.patel@gmail.com', 'scrypt:32768:8:1$K12345$pbkdf2_sha256_mock_hash_or_plain_password123', 'patient', 'Aisha', 'Patel', '+1 (555) 400-0010', 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150', 1);

-- 3. Insert Doctors
INSERT INTO doctors (id, user_id, department_id, license_number, specialization, qualification, experience_years, consultation_fee, room_number, bio, available_days, is_active) VALUES
(1, 2, 1, 'MD-CARD-88421', 'Interventional Cardiology', 'MD, FACC, Harvard Medical School', 14, 180.00, 'Room 304-A', 'Specializes in coronary artery disease, heart failure prediction, and AI-assisted echocardiogram analysis.', 'Mon,Tue,Wed,Thu,Fri', 1),
(2, 3, 2, 'MD-ENDO-99312', 'Endocrinology & Metabolism', 'MD, PhD, Johns Hopkins Medicine', 11, 160.00, 'Room 210-B', 'Expert in complex type-2 diabetes regression models, insulin resistance diagnostics, and personalized nutrition plans.', 'Mon,Wed,Fri', 1),
(3, 4, 3, 'MD-NEUR-77290', 'Vascular Neurology & Stroke', 'MD, FAAN, Stanford Health Care', 16, 210.00, 'Room 408-C', 'Pioneer in ischemic stroke risk stratification, acute neurological intervention, and cerebral perfusion imaging.', 'Tue,Thu,Sat', 1);

-- Update Head Doctors for Departments
UPDATE departments SET head_doctor_id = 1 WHERE id = 1;
UPDATE departments SET head_doctor_id = 2 WHERE id = 2;
UPDATE departments SET head_doctor_id = 3 WHERE id = 3;

-- 4. Insert Nurses (with Room and Duty Assignment)
INSERT INTO nurses (id, user_id, department_id, license_number, qualification, shift_timing, assigned_room, duty_status, is_active) VALUES
(1, 5, 1, 'RN-CRIT-55102', 'BSN, RN, CCRN Certified', 'Morning (06:00 - 14:00)', 'Cardiac Care Unit - CCU 301', 'On Duty', 1),
(2, 6, 4, 'RN-MED-66291', 'BSN, RN, Emergency Specialist', 'Evening (14:00 - 22:00)', 'Ward 2 - Rooms 201-208', 'On Duty', 1);

-- 5. Insert Patients
INSERT INTO patients (id, user_id, patient_code, date_of_birth, gender, blood_group, marital_status, address, city, emergency_contact_name, emergency_contact_phone, insurance_provider, insurance_policy_number, allergies, assigned_doctor_id, assigned_room, is_active) VALUES
(1, 7, 'PAT-2026-001', '1974-05-14', 'Male', 'O+', 'Married', '742 Evergreen Terrace', 'Springfield, IL', 'Jane Doe (Wife)', '+1 (555) 444-1234', 'Blue Cross Blue Shield', 'BCBS-99882211', 'Penicillin, Shellfish', 1, 'Room 301-Bed A', 1),
(2, 8, 'PAT-2026-002', '1968-11-23', 'Female', 'A+', 'Single', '1088 Ocean Drive', 'Miami, FL', 'Carlos Garcia (Son)', '+1 (555) 444-5678', 'Aetna Health Care', 'AET-77441199', 'Sulfa drugs, Aspirin', 3, 'Room 408-Bed B', 1),
(3, 9, 'PAT-2026-003', '1989-03-08', 'Male', 'B+', 'Married', '452 Pine Valley Rd', 'Austin, TX', 'Linda Chen (Sister)', '+1 (555) 444-9900', 'UnitedHealthcare', 'UHC-33221100', 'None known', 2, 'Outpatient', 1),
(4, 10, 'PAT-2026-004', '1982-08-19', 'Female', 'AB-', 'Married', '224 Sunset Boulevard', 'San Jose, CA', 'Dev Patel (Husband)', '+1 (555) 444-7711', 'Cigna Global Health', 'CIG-55667788', 'Latex, Codeine', 2, 'Outpatient', 1);

-- 6. Insert Appointments
INSERT INTO appointments (id, appointment_code, patient_id, doctor_id, department_id, appointment_date, appointment_time, status, priority, symptoms, doctor_notes) VALUES
(1, 'APT-2026-001', 1, 1, 1, '2026-08-10', '09:30:00', 'Confirmed', 'Urgent', 'Intermittent chest tightness, shortness of breath on exertion, mild palpitations.', 'Scheduled for ECG review and AI cardiovascular risk assessment.'),
(2, 'APT-2026-002', 2, 3, 3, '2026-08-11', '11:00:00', 'Scheduled', 'Urgent', 'Transient tingling on left arm, episodic dizziness, elevated blood pressure.', 'Ordered cerebral vascular doppler and stroke risk analysis.'),
(3, 'APT-2026-003', 3, 2, 2, '2026-08-12', '14:15:00', 'Confirmed', 'Normal', 'Persistent thirst, polyuria, fasting blood sugar tracking around 155 mg/dL.', 'Quarterly HbA1c evaluation and diabetes medication titration.'),
(4, 'APT-2026-004', 4, 2, 2, '2026-08-14', '16:00:00', 'Scheduled', 'Normal', 'Fatigue, sudden weight changes, routine metabolic panel follow-up.', 'Thyroid function test and lifestyle optimization review.');

-- 7. Insert Vitals (Recorded by Nurse Emily Watson)
INSERT INTO vitals (id, patient_id, recorded_by_user_id, temperature, blood_pressure_systolic, blood_pressure_diastolic, heart_rate, respiratory_rate, spo2, weight, height, bmi, blood_glucose, notes, recorded_at) VALUES
(1, 1, 5, 98.6, 142, 92, 84, 18, 97, 88.50, 178.00, 27.9, 118.0, 'Patient reports mild chest discomfort after climbing stairs. BP slightly elevated.', '2026-08-07 08:30:00'),
(2, 1, 5, 98.4, 138, 88, 78, 16, 98, 88.20, 178.00, 27.8, 110.0, 'Morning vitals stabilizing. Resting heart rate normalized.', '2026-08-08 07:45:00'),
(3, 2, 5, 99.1, 165, 105, 92, 20, 96, 74.00, 162.00, 28.2, 145.0, 'Significant hypertension observed. SpO2 within acceptable range. Alerted Dr. Rostova.', '2026-08-08 08:15:00'),
(4, 3, 6, 98.7, 122, 78, 70, 15, 99, 79.50, 180.00, 24.5, 162.0, 'Elevated fasting blood sugar. Vitals otherwise stable.', '2026-08-07 15:20:00'),
(5, 4, 6, 98.2, 118, 74, 68, 16, 99, 62.00, 165.00, 22.8, 94.0, 'All parameters in optimal physiological ranges.', '2026-08-07 16:00:00');

-- 8. Insert Medical Records (EHR History)
INSERT INTO medical_records (id, patient_id, doctor_id, appointment_id, diagnosis, symptoms, treatment_plan, prescription, lab_tests_ordered, follow_up_date) VALUES
(1, 1, 1, 1, 'Stage 1 Hypertension & Suspected Coronary Artery Stenosis', 'Chest tightness, exertional dyspnea, fatigue', 'Low-sodium Mediterranean diet, daily 30-min walking, pharmacological control.', 'Atorvastatin 20mg Once Daily (Night), Amlodipine 5mg Morning', 'Lipid Panel, High-Sensitivity Troponin-I, 12-Lead ECG', '2026-08-25'),
(2, 2, 3, 2, 'Transient Ischemic Attack (TIA) Prodrome / Essential Hypertension', 'Transient numbness in left hand, slurred speech lasting 4 minutes, migraine aura.', 'Immediate blood pressure regulation, antiplatelet therapy, carotid ultrasound.', 'Clopidogrel (Plavix) 75mg Daily, Lisinopril 20mg Daily', 'Carotid Doppler Ultrasound, Brain MRI / MRA, Serum Electrolytes', '2026-08-22'),
(3, 3, 2, 3, 'Type 2 Diabetes Mellitus (Uncontrolled Fasting Hyperglycemia)', 'Polydipsia, polyuria, blurred vision after high-carb meals.', 'Nutritional carbohydrate restriction, continuous glucose monitoring (CGM).', 'Metformin 850mg Twice Daily with meals, Empagliflozin 10mg Daily', 'HbA1c, Fasting Insulin, Comprehensive Metabolic Panel', '2026-09-01');

-- 9. Insert AI Predictions (Logged inferences with model versions and risk breakdown)
INSERT INTO predictions (id, patient_id, doctor_id, disease_type, model_version, risk_score, risk_level, prediction_result, confidence_score, input_features, feature_importance, clinical_recommendation, doctor_feedback) VALUES
(1, 1, 1, 'Heart Disease', 'v1.2.0-rf-xgboost', 78.45, 'High', 'Positive Risk Indicator', 89.20,
 '{"age": 52, "sex": 1, "cp": 2, "trestbps": 142, "chol": 268, "fbs": 0, "restecg": 1, "thalach": 138, "exang": 1, "oldpeak": 2.3, "slope": 1, "ca": 1, "thal": 2}',
 '{"chol": "+28%", "oldpeak": "+24%", "trestbps": "+19%", "thalach": "-12%", "age": "+11%"}',
 'High probability of significant coronary artery plaque. Immediate stress echocardiogram and statin intensification advised.', 'Confirmed'),

(2, 2, 3, 'Stroke', 'v1.1.0-xgboost-balanced', 84.10, 'Critical', 'Critical Stroke Risk', 92.50,
 '{"age": 57, "hypertension": 1, "heart_disease": 0, "ever_married": 0, "work_type": "Private", "Residence_type": "Urban", "avg_glucose_level": 145.2, "bmi": 28.2, "smoking_status": "formerly smoked"}',
 '{"hypertension": "+36%", "avg_glucose_level": "+22%", "age": "+21%", "bmi": "+12%"}',
 'Imminent risk of ischemic cerebrovascular event. Initiate urgent carotid ultrasound and dual antiplatelet therapy under supervision.', 'Confirmed'),

(3, 3, 2, 'Diabetes', 'v1.0.4-gradient-boost', 68.30, 'Moderate', 'High Probability Type-2 Diabetes', 86.75,
 '{"pregnancies": 0, "glucose": 162, "blood_pressure": 78, "skin_thickness": 28, "insulin": 140, "bmi": 24.5, "dpf": 0.627, "age": 37}',
 '{"glucose": "+48%", "insulin": "+20%", "dpf": "+14%", "bmi": "+10%"}',
 'Blood glucose and genetic diabetes pedigree indicator suggest early insulin resistance. Begin metformin and carbohydrate thresholding.', 'Confirmed');

-- 10. Insert Notifications (Live reminders for patients & staff alerts)
INSERT INTO notifications (id, user_id, title, message, type, is_read, action_url) VALUES
(1, 7, 'Appointment Reminder: Cardiology Consultation', 'Your upcoming consultation with Dr. Sarah Chen is scheduled for August 10, 2026 at 09:30 AM in Room 304-A.', 'Appointment', 0, '/patient/appointments'),
(2, 7, 'AI Health Analysis Ready', 'Dr. Sarah Chen has completed your Heart Disease AI risk assessment. View your clinical breakdown and prevention steps.', 'AI Alert', 0, '/patient/predictions'),
(3, 8, 'Urgent: Stroke Risk Protocol Follow-up', 'Dr. Elena Rostova has updated your treatment plan based on today’s critical AI assessment. Please review immediately.', 'AI Alert', 0, '/patient/predictions'),
(4, 8, 'Appointment Scheduled: Neurology Review', 'Consultation with Dr. Elena Rostova confirmed for August 11, 2026 at 11:00 AM in Room 408-C.', 'Appointment', 0, '/patient/appointments'),
(5, 2, 'New Patient Assigned: John Doe', 'Patient John Doe has been assigned to Cardiology for elevated BP and exertional chest pain.', 'General', 1, '/doctor/patients'),
(6, 5, 'Critical Vitals Alert: Room 408-Bed B', 'Patient Maria Garcia recorded BP 165/105 mmHg. Notification dispatched to attending neurologist.', 'Vital Warning', 1, '/nurse/vitals');

-- 11. Insert Audit Logs
INSERT INTO audit_logs (id, user_id, action, entity_type, entity_id, details, ip_address) VALUES
(1, 1, 'SYSTEM_INIT', 'System', 1, 'KAIre Health Enterprise Hospital Management System initialized with ML pipeline.', '127.0.0.1'),
(2, 2, 'RUN_AI_PREDICTION', 'Prediction', 1, 'Dr. Sarah Chen generated Heart Disease AI risk prediction for Patient #1 (Score: 78.45%).', '192.168.1.42'),
(3, 5, 'RECORD_VITALS', 'Vital', 3, 'Nurse Emily Watson recorded abnormal blood pressure (165/105 mmHg) for Patient #2.', '192.168.1.77'),
(4, 1, 'UPDATE_DOCTOR', 'Doctor', 1, 'Administrator updated consultation fees and department room assignment for Dr. Sarah Chen.', '127.0.0.1');
