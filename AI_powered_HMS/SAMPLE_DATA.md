# Sample Data — Insert 2–3 Values Per Table

Run these SQL statements in **MySQL Workbench** after creating all tables.
Execute them **in order** (top to bottom) so foreign keys resolve correctly.

---

## 1. roles (already inserted by schema)
```sql
-- Already done by CREATE TABLE script:
INSERT INTO roles (role_name) VALUES ('admin'),('doctor'),('nurse'),('patient');
```
> role_id: 1=admin, 2=doctor, 3=nurse, 4=patient

---

## 2. departments
```sql
INSERT INTO departments (dept_name, description) VALUES
('Cardiology',       'Heart disease diagnosis and treatment'),
('Neurology',        'Brain, spinal cord and stroke treatment'),
('General Medicine', 'Diabetes, general health and checkups');
```
> dept_id: 1=Cardiology, 2=Neurology, 3=General Medicine

---

## 3. users
```sql
-- Admin
INSERT INTO users (name, email, password, role_id) VALUES
('Admin User',        'admin@hospital.com',   'admin123',  1);

-- Doctors (one per department)
INSERT INTO users (name, email, password, role_id) VALUES
('Dr. Raj Sharma',    'heart@hospital.com',   'doctor123', 2),
('Dr. Neha Patel',    'neuro@hospital.com',   'doctor123', 2),
('Dr. Amit Verma',    'general@hospital.com', 'doctor123', 2);

-- Nurses
INSERT INTO users (name, email, password, role_id) VALUES
('Nurse Priya',       'priya@hospital.com',   'nurse123',  3),
('Nurse Sunita',      'sunita@hospital.com',  'nurse123',  3);

-- Patients
INSERT INTO users (name, email, password, role_id) VALUES
('Ramesh Patel',      'ramesh@gmail.com',     'patient123',4),
('Anita Shah',        'anita@gmail.com',      'patient123',4),
('Mohit Verma',       'mohit@gmail.com',      'patient123',4);
```
> Run `SELECT user_id, name, email FROM users;` to confirm IDs before next step.

---

## 4. doctors
```sql
-- Assuming user_ids: Raj=2, Neha=3, Amit=4 (check with SELECT above)
INSERT INTO doctors (user_id, dept_id, specialization, experience, phone) VALUES
(2, 1, 'Heart Specialist',  10, '9876541001'),   -- Cardiology
(3, 2, 'Brain Specialist',   8, '9876541002'),   -- Neurology
(4, 3, 'General Physician', 12, '9876541003');   -- General Medicine
```

---

## 5. nurses
```sql
-- Assuming user_ids: Priya=5, Sunita=6
INSERT INTO nurses (user_id, dept_id, phone) VALUES
(5, 1, '9876542001'),   -- Cardiology nurse
(6, 2, '9876542002');   -- Neurology nurse
```

---

## 6. patients
```sql
-- Assuming user_ids: Ramesh=7, Anita=8, Mohit=9
INSERT INTO patients (user_id, age, gender, phone, address) VALUES
(7, 45, 'male',   '9000000001', 'Surat, Gujarat'),
(8, 52, 'female', '9000000002', 'Ahmedabad, Gujarat'),
(9, 38, 'male',   '9000000003', 'Vadodara, Gujarat');
```

---

## 7. vitals
```sql
-- Assuming patient_ids: Ramesh=1, Anita=2, Mohit=3
-- Assuming nurse_ids:   Priya=1,  Sunita=2
INSERT INTO vitals (patient_id, blood_pressure, cholesterol, glucose, heart_rate, bmi, recorded_by) VALUES
(1, 130, 220, 140, 80,  25.5, 1),
(2, 145, 240, 160, 85,  28.2, 2),
(3, 120, 210, 110, 75,  23.0, 1);
```

---

## 8. predictions
```sql
-- Assuming patient_ids: 1,2,3  |  doctor_ids: 1(heart),2(neuro),3(general)
INSERT INTO predictions (patient_id, doctor_id, disease_type, prediction_result, probability) VALUES
(1, 1, 'heart',    'High Risk',          0.82),
(2, 3, 'diabetes', 'Diabetes Detected',  0.76),
(3, 2, 'stroke',   'Low Risk',           0.21);
```

---

## 9. prediction_inputs
```sql
-- prediction_id matches the 3 rows above (likely 1, 2, 3)
INSERT INTO prediction_inputs (prediction_id, age, sex, cp, trestbps, chol, thalach, oldpeak) VALUES
(1, 45, 1, 3, 130, 220, 150, 2.3),
(2, 52, 0, 2, 145, 240, 140, 1.5),
(3, 38, 1, 1, 120, 210, 160, 0.8);
```

---

## Verify All Tables
```sql
SELECT * FROM roles;
SELECT * FROM departments;
SELECT * FROM users;
SELECT * FROM doctors;
SELECT * FROM nurses;
SELECT * FROM patients;
SELECT * FROM vitals;
SELECT * FROM predictions;
SELECT * FROM prediction_inputs;
```

---

## Login Credentials Summary

| Email                  | Password   | Role              | Prediction Access     |
|------------------------|------------|-------------------|-----------------------|
| admin@hospital.com     | admin123   | Admin             | Departments, Users    |
| heart@hospital.com     | doctor123  | Doctor (Cardiology)   | ❤️ Heart only     |
| neuro@hospital.com     | doctor123  | Doctor (Neurology)    | 🧠 Stroke only    |
| general@hospital.com   | doctor123  | Doctor (General Med)  | 🩸 Diabetes only  |
| priya@hospital.com     | nurse123   | Nurse             | Vitals, Records       |
| ramesh@gmail.com       | patient123 | Patient           | Own results only      |
