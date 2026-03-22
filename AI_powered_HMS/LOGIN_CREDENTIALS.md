# Login Credentials — AI Hospital Management System
login ke liye general wala doctor kholke ke check kre 


All credentials are based on the sample data inserted via `SAMPLE_DATA.md`.
Use these to test and navigate all roles in the system.

---

## Admin

| Field    | Value                  |
|----------|------------------------|
| Email    | admin@hospital.com     |
| Password | admin123               |
| Role     | Admin                  |
| Access   | Departments, All Users |

---

## Doctors

> Each doctor can only access the prediction tool for their own department.

| Name            | Email                  | Password  | Department       | Can Predict       |
|-----------------|------------------------|-----------|------------------|-------------------|
| Dr. Raj Sharma  | heart@hospital.com     | doctor123 | Cardiology       | ❤️ Heart Disease  |
| Dr. Neha Patel  | neuro@hospital.com     | doctor123 | Neurology        | 🧠 Stroke         |
| Dr. Amit Verma  | general@hospital.com   | doctor123 | General Medicine | 🩸 Diabetes       |

---

## Nurses

| Name         | Email               | Password | Department  | Access                    |
|--------------|---------------------|----------|-------------|---------------------------|
| Nurse Priya  | priya@hospital.com  | nurse123 | Cardiology  | Record Vitals, View Records |
| Nurse Sunita | sunita@hospital.com | nurse123 | Neurology   | Record Vitals, View Records |

---

## Patients

> Patients can self-register from the Register page.
> These 3 are pre-inserted via sample data SQL.

| Name         | Email             | Password   | Access                  |
|--------------|-------------------|------------|-------------------------|
| Ramesh Patel | ramesh@gmail.com  | patient123 | View own prediction results |
| Anita Shah   | anita@gmail.com   | patient123 | View own prediction results |
| Mohit Verma  | mohit@gmail.com   | patient123 | View own prediction results |

---

## Quick Test Flow

### Test Heart Prediction
1. Login → `heart@hospital.com` / `doctor123`
2. Dashboard → Click **Heart Prediction**
3. Select a patient → Fill in values → Click **Predict**

### Test Diabetes Prediction
1. Login → `general@hospital.com` / `doctor123`
2. Dashboard → Click **Diabetes Prediction**
3. Select a patient → Fill in values → Click **Predict**

### Test Stroke Prediction
1. Login → `neuro@hospital.com` / `doctor123`
2. Dashboard → Click **Stroke Prediction**
3. Select a patient → Fill in values → Click **Predict**

### Test Nurse Vitals
1. Login → `priya@hospital.com` / `nurse123`
2. Dashboard → Click **Record Vitals**
3. Select patient → Enter BP, glucose, cholesterol → Save

### Test Patient Results
1. Login → `ramesh@gmail.com` / `patient123`
2. Dashboard → Click **My Prediction Results**
3. See all predictions made by doctors for this patient

### Test Admin
1. Login → `admin@hospital.com` / `admin123`
2. Dashboard → View stats (users, departments, predictions)
3. Click **Departments** → Add or delete departments
4. Click **All Users** → View all registered users

---

## Access Control Rules

| Role    | Heart Prediction | Diabetes Prediction | Stroke Prediction | Vitals | Admin Panel |
|---------|:-:|:-:|:-:|:-:|:-:|
| Admin            | ✗ | ✗ | ✗ | ✗ | ✅ |
| Doctor-Cardiology| ✅ | ✗ | ✗ | ✗ | ✗ |
| Doctor-General   | ✗ | ✅ | ✗ | ✗ | ✗ |
| Doctor-Neurology | ✗ | ✗ | ✅ | ✗ | ✗ |
| Nurse            | ✗ | ✗ | ✗ | ✅ | ✗ |
| Patient          | ✗ | ✗ | ✗ | ✗ | ✗ |

> If a doctor from the wrong department tries to access another prediction page,
> they will see an **"Access Denied"** page automatically.

---

## Sample Prediction Input Values for Testing

### Heart Disease (login as heart@hospital.com)
| Field       | Sample Value |
|-------------|-------------|
| Age         | 52          |
| Sex         | 1 (Male)    |
| CP          | 3           |
| Trestbps    | 130         |
| Chol        | 220         |
| Thalch      | 150         |
| Exang       | 0           |
| Oldpeak     | 2.3         |
| Slope       | 0           |
| CA          | 0           |
| Thal        | 1           |

### Diabetes (login as general@hospital.com)
| Field                    | Sample Value |
|--------------------------|-------------|
| Pregnancies              | 2           |
| Glucose                  | 148         |
| Blood Pressure           | 72          |
| Skin Thickness           | 35          |
| Insulin                  | 0           |
| BMI                      | 33.6        |
| Diabetes Pedigree Func   | 0.627       |
| Age                      | 50          |

### Stroke (login as neuro@hospital.com)
| Field          | Sample Value |
|----------------|-------------|
| Gender         | 1 (Male)    |
| Age            | 67          |
| Hypertension   | 0           |
| Heart Disease  | 1           |
| Ever Married   | 1 (Yes)     |
| Work Type      | 3 (Private) |
| Residence Type | 1 (Urban)   |
| Avg Glucose    | 228.69      |
| BMI            | 36.6        |
| Smoking Status | 0 (Formerly)|
