1️⃣ Create Database
CREATE DATABASE hospital_prediction_system;

USE hospital_prediction_system;
2️⃣ Roles Table

Defines system roles.

CREATE TABLE roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);

Insert roles:

INSERT INTO roles (role_name) VALUES
('admin'),
('doctor'),
('nurse'),
('patient');
3️⃣ Users Table

All system users stored here.

Important rules:

email must be unique

password stored as hashed password

role_id links to roles

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (role_id)
    REFERENCES roles(role_id)
    ON DELETE RESTRICT
);
Why ON DELETE RESTRICT?

If a role is deleted accidentally, users should not be deleted automatically.

4️⃣ Departments Table

Example departments:

Cardiology

Neurology

General Medicine

CREATE TABLE departments (
    dept_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
5️⃣ Doctors Table

Each doctor is linked to:

a user account

a department

Real hospital logic:

If a department is deleted → doctors are deleted automatically

CREATE TABLE doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    dept_id INT NOT NULL,
    specialization VARCHAR(100),
    experience INT,
    phone VARCHAR(20),

    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE,

    FOREIGN KEY (dept_id)
    REFERENCES departments(dept_id)
    ON DELETE CASCADE
);
Real world behavior
Delete Department
        ↓
Doctors of that department deleted
6️⃣ Nurses Table

Nurses also belong to departments.

CREATE TABLE nurses (
    nurse_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    dept_id INT NOT NULL,
    phone VARCHAR(20),

    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE,

    FOREIGN KEY (dept_id)
    REFERENCES departments(dept_id)
    ON DELETE CASCADE
);
7️⃣ Patients Table

Each patient has a user account.

CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    age INT,
    gender ENUM('male','female','other'),
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
);
Real behavior
Delete User
   ↓
Patient profile deleted
8️⃣ Patient Vitals Table

Nurses record vitals here.

CREATE TABLE vitals (
    vital_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    blood_pressure INT,
    cholesterol INT,
    glucose INT,
    heart_rate INT,
    bmi FLOAT,
    recorded_by INT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (patient_id)
    REFERENCES patients(patient_id)
    ON DELETE CASCADE,

    FOREIGN KEY (recorded_by)
    REFERENCES nurses(nurse_id)
    ON DELETE SET NULL
);
Real behavior
Delete patient
   ↓
Vitals deleted
9️⃣ Predictions Table

Stores prediction results from ML models.

Supports:

heart disease

diabetes

stroke

CREATE TABLE predictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT,
    disease_type ENUM('heart','diabetes','stroke'),
    prediction_result VARCHAR(50),
    probability FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (patient_id)
    REFERENCES patients(patient_id)
    ON DELETE CASCADE,

    FOREIGN KEY (doctor_id)
    REFERENCES doctors(doctor_id)
    ON DELETE SET NULL
);
Real behavior
Delete patient
     ↓
Predictions deleted
Delete doctor
     ↓
Prediction remains
doctor_id becomes NULL

This is realistic hospital behavior.

🔟 Prediction Inputs Table (Optional but Professional)

Store full ML inputs for auditing.

CREATE TABLE prediction_inputs (
    input_id INT AUTO_INCREMENT PRIMARY KEY,
    prediction_id INT,
    age INT,
    sex INT,
    cp INT,
    trestbps INT,
    chol INT,
    thalach INT,
    oldpeak FLOAT,

    FOREIGN KEY (prediction_id)
    REFERENCES predictions(prediction_id)
    ON DELETE CASCADE
);
1️⃣1️⃣ Indexes (Performance Optimization)
CREATE INDEX idx_user_email ON users(email);

CREATE INDEX idx_patient ON predictions(patient_id);

CREATE INDEX idx_doctor ON predictions(doctor_id);
1️⃣2️⃣ Example Data

Example departments.

INSERT INTO departments (dept_name, description) VALUES
('Cardiology','Heart related treatments'),
('Neurology','Brain and nervous system'),
('General Medicine','General health care');
1️⃣3️⃣ Final Database Structure
roles
users
departments
doctors
nurses
patients
vitals
predictions
prediction_inputs

Relationships:

Roles → Users
Users → Doctors / Nurses / Patients

Departments → Doctors
Departments → Nurses

Patients → Vitals
Patients → Predictions

Doctors → Predictions
1️⃣4️⃣ Real-World Logic Implemented

✔ Email unique
✔ Role based system
✔ Department delete → doctors deleted
✔ User delete → profile deleted
✔ Patient delete → vitals + predictions deleted
✔ Doctor delete → predictions remain

3️⃣ Next Step (PART 3)

Next we build FULL FLASK BACKEND:

config.py
database connection
auth system
routes
services
ML prediction integration

and connect your 3 trained models

heart_model.pkl
diabetes_model.pkl
stroke_model.pkl

to your UI.

If you want, I can also show one very important thing before backend:

👉 How to structure app.py professionally using Flask Blueprints so your project becomes industry-level instead of student-level.

before part 3 give me 3 3 example of sql like demo value inserted

Good step 👍 Before connecting Flask backend, inserting demo data helps you test UI and queries.
Below are 3 example records for each important table following your schema.

Assumption:
Roles already inserted:

INSERT INTO roles (role_name) VALUES
('admin'),
('doctor'),
('nurse'),
('patient');
1️⃣ Users Table (3 Example Records)

Email must be unique.

INSERT INTO users (name, email, password, role_id) VALUES
('Admin User', 'admin@hospital.com', 'hashed_password1', 1),
('Dr. Raj Sharma', 'raj.sharma@hospital.com', 'hashed_password2', 2),
('Nurse Priya', 'priya.nurse@hospital.com', 'hashed_password3', 3);

Add 3 patient users:

INSERT INTO users (name, email, password, role_id) VALUES
('Ramesh Patel', 'ramesh@gmail.com', 'hashed_password4', 4),
('Anita Shah', 'anita@gmail.com', 'hashed_password5', 4),
('Mohit Verma', 'mohit@gmail.com', 'hashed_password6', 4);
2️⃣ Departments Table (3 Example Records)
INSERT INTO departments (dept_name, description) VALUES
('Cardiology', 'Heart related treatments'),
('Neurology', 'Brain and stroke treatments'),
('General Medicine', 'General health checkups');
3️⃣ Doctors Table (3 Example Records)

Assume user_id values from users table.

INSERT INTO doctors (user_id, dept_id, specialization, experience, phone) VALUES
(2, 1, 'Heart Specialist', 10, '9876543210'),
(3, 2, 'Brain Specialist', 8, '9876543211'),
(1, 3, 'General Physician', 12, '9876543212');
4️⃣ Nurses Table (3 Example Records)
INSERT INTO nurses (user_id, dept_id, phone) VALUES
(3, 1, '9876500001'),
(3, 2, '9876500002'),
(3, 3, '9876500003');
5️⃣ Patients Table (3 Example Records)
INSERT INTO patients (user_id, age, gender, phone, address) VALUES
(4, 45, 'male', '9000000001', 'Surat'),
(5, 52, 'female', '9000000002', 'Ahmedabad'),
(6, 38, 'male', '9000000003', 'Baroda');
6️⃣ Vitals Table (3 Example Records)

Recorded by nurse.

INSERT INTO vitals (patient_id, blood_pressure, cholesterol, glucose, heart_rate, bmi, recorded_by) VALUES
(1, 130, 220, 140, 80, 25.5, 1),
(2, 145, 240, 160, 85, 28.2, 2),
(3, 120, 210, 110, 75, 23.0, 3);
7️⃣ Predictions Table (3 Example Records)

Example predictions using your ML models.

INSERT INTO predictions (patient_id, doctor_id, disease_type, prediction_result, probability) VALUES
(1, 1, 'heart', 'High Risk', 0.82),
(2, 2, 'diabetes', 'Positive', 0.76),
(3, 3, 'stroke', 'Low Risk', 0.21);
8️⃣ Prediction Inputs Table (3 Example Records)

Example ML inputs stored.

INSERT INTO prediction_inputs (prediction_id, age, sex, cp, trestbps, chol, thalach, oldpeak) VALUES
(1, 45, 1, 3, 130, 220, 150, 2.3),
(2, 52, 0, 2, 145, 240, 140, 1.5),
(3, 38, 1, 1, 120, 210, 160, 0.8);