-- ==============================================================================
-- KAIre Health - AI-Powered Hospital Management System Database Schema
-- Compatible with MySQL 8.0+ and SQLite (ANSI-SQL compatible dialect)
-- ==============================================================================

-- 1. Users Table (Core Auth & Roles: admin, doctor, nurse, patient)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'doctor', 'nurse', 'patient') NOT NULL DEFAULT 'patient',
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    avatar_url VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Departments Table
CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    code VARCHAR(20) NOT NULL UNIQUE,
    description TEXT,
    head_doctor_id INT NULL,
    location_floor VARCHAR(50),
    contact_phone VARCHAR(20),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 3. Doctors Table
CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    department_id INT NOT NULL,
    license_number VARCHAR(50) NOT NULL UNIQUE,
    specialization VARCHAR(100) NOT NULL,
    qualification VARCHAR(100),
    experience_years INT DEFAULT 0,
    consultation_fee DECIMAL(10,2) DEFAULT 0.00,
    room_number VARCHAR(20),
    bio TEXT,
    available_days VARCHAR(100) DEFAULT 'Mon,Tue,Wed,Thu,Fri',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE RESTRICT
);

-- 4. Nurses Table (includes Room & Duty Assignment)
CREATE TABLE IF NOT EXISTS nurses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    department_id INT NOT NULL,
    license_number VARCHAR(50) NOT NULL UNIQUE,
    qualification VARCHAR(100),
    shift_timing ENUM('Morning (06:00 - 14:00)', 'Evening (14:00 - 22:00)', 'Night (22:00 - 06:00)') NOT NULL DEFAULT 'Morning (06:00 - 14:00)',
    assigned_room VARCHAR(50) DEFAULT 'Ward A - Room 102',
    duty_status ENUM('On Duty', 'Break', 'Off Duty', 'Emergency Dispatch') NOT NULL DEFAULT 'On Duty',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE RESTRICT
);

-- 5. Patients Table
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    patient_code VARCHAR(30) NOT NULL UNIQUE,
    date_of_birth DATE NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    blood_group VARCHAR(10),
    marital_status VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    insurance_provider VARCHAR(100),
    insurance_policy_number VARCHAR(50),
    allergies TEXT,
    assigned_doctor_id INT NULL,
    assigned_room VARCHAR(50) NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_doctor_id) REFERENCES doctors(id) ON DELETE SET NULL
);

-- 6. Appointments Table
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_code VARCHAR(30) NOT NULL UNIQUE,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    department_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status ENUM('Scheduled', 'Confirmed', 'In-Progress', 'Completed', 'Cancelled', 'Rescheduled') NOT NULL DEFAULT 'Scheduled',
    priority ENUM('Low', 'Normal', 'Urgent', 'Emergency') NOT NULL DEFAULT 'Normal',
    symptoms TEXT,
    doctor_notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE RESTRICT
);

-- 7. Vitals Table (Recorded by Nurse or Doctor)
CREATE TABLE IF NOT EXISTS vitals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    recorded_by_user_id INT NOT NULL,
    temperature DECIMAL(4,1) NOT NULL COMMENT 'in Fahrenheit (e.g. 98.6)',
    blood_pressure_systolic INT NOT NULL COMMENT 'e.g. 120',
    blood_pressure_diastolic INT NOT NULL COMMENT 'e.g. 80',
    heart_rate INT NOT NULL COMMENT 'BPM (e.g. 72)',
    respiratory_rate INT DEFAULT 16,
    spo2 INT NOT NULL COMMENT 'Oxygen Saturation % (e.g. 98)',
    weight DECIMAL(5,2) NOT NULL COMMENT 'in kg (e.g. 70.5)',
    height DECIMAL(5,2) COMMENT 'in cm (e.g. 175.0)',
    bmi DECIMAL(4,1) COMMENT 'calculated BMI',
    blood_glucose DECIMAL(5,1) COMMENT 'mg/dL (e.g. 95.0)',
    notes TEXT,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (recorded_by_user_id) REFERENCES users(id) ON DELETE RESTRICT
);

-- 8. Medical Records Table (EHR)
CREATE TABLE IF NOT EXISTS medical_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_id INT NULL,
    diagnosis VARCHAR(255) NOT NULL,
    symptoms TEXT,
    treatment_plan TEXT,
    prescription TEXT,
    lab_tests_ordered TEXT,
    follow_up_date DATE,
    attachments_url VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE SET NULL
);

-- 9. AI Predictions Table (Stores Heart, Diabetes, Stroke inference records & model versions)
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    disease_type ENUM('Heart Disease', 'Diabetes', 'Stroke') NOT NULL,
    model_version VARCHAR(50) NOT NULL DEFAULT 'v1.0.0-xgb',
    risk_score DECIMAL(5,2) NOT NULL COMMENT 'Percentage risk (0.00 to 100.00)',
    risk_level ENUM('Low', 'Moderate', 'High', 'Critical') NOT NULL,
    prediction_result VARCHAR(100) NOT NULL COMMENT 'e.g. Positive / Negative / High Probability',
    confidence_score DECIMAL(5,2) NOT NULL,
    input_features JSON NOT NULL COMMENT 'Raw feature key-value pairs used for inference',
    feature_importance JSON NULL COMMENT 'Top contributing features / SHAP values',
    clinical_recommendation TEXT,
    doctor_feedback ENUM('Pending Review', 'Confirmed', 'False Positive', 'Inconclusive') DEFAULT 'Pending Review',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
);

-- 10. Notifications Table (Patient reminders, appointment notifications, urgent alerts)
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    type ENUM('Appointment', 'AI Alert', 'Vital Warning', 'General', 'System') NOT NULL DEFAULT 'General',
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    action_url VARCHAR(255) NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 11. Audit Logs Table (Admin traceability for all CRUD actions)
CREATE TABLE IF NOT EXISTS audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INT NULL,
    details TEXT,
    ip_address VARCHAR(45),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Indexes for high-performance querying
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_patients_code ON patients(patient_code);
CREATE INDEX idx_appointments_date ON appointments(appointment_date, status);
CREATE INDEX idx_vitals_patient ON vitals(patient_id, recorded_at);
CREATE INDEX idx_predictions_patient ON predictions(patient_id, disease_type);
CREATE INDEX idx_notifications_user ON notifications(user_id, is_read);
CREATE INDEX idx_audit_created ON audit_logs(created_at);
