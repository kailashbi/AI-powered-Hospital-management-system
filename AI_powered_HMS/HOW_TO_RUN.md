login ke liye general wala doctor kholke ke check kre 

# HOW TO RUN — AI-Powered Hospital Management System

---

## Prerequisites
- Python 3.9 or higher
- MySQL Server running locally
- MySQL Workbench (to run SQL queries)

---

## STEP 1 — MySQL Database Setup

1. Open **MySQL Workbench**
2. Run the full SQL from `sql_readme.md` to create all tables
3. Then open **`SAMPLE_DATA.md`** and run those INSERT statements
   to add sample departments, users, doctors, nurses, patients, and predictions

> ⚠️ **Important:** Departments must be named exactly:
> - `Cardiology`
> - `Neurology`
> - `General Medicine`
> (case-sensitive matching is used for role-based access)

---

## STEP 2 — Update Database Credentials

Open `config.py` and set your MySQL password:

```python
DB_HOST     = "localhost"
DB_USER     = "root"
DB_PASSWORD = "your_mysql_password_here"
DB_NAME     = "hospital_prediction_system"
```

---

## STEP 3 — Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

---

## STEP 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs: Flask, mysql-connector-python, scikit-learn, xgboost, pandas, numpy, joblib

---

## STEP 5 — Train All 3 ML Models (Run ONCE)

```bash
python train_all_models.py
```

This trains three models one by one and saves them in the `model/` folder:

| Model File                    | Algorithm           | Disease        |
|-------------------------------|---------------------|----------------|
| `model/heart_model.pkl`       | Random Forest       | Heart Disease  |
| `model/diabetes_model.pkl`    | Logistic Regression | Diabetes       |
| `model/diabetes_scaler.pkl`   | StandardScaler      | Diabetes       |
| `model/stroke_model.pkl`      | XGBoost             | Stroke         |

Accuracy reports are also saved as `.txt` files in `model/`:
- `model/heart_model_accuracy.txt`
- `model/diabetes_model_accuracy.txt`
- `model/stroke_model_accuracy.txt`

Expected accuracies:
- Heart:    ~85–88%
- Diabetes: ~77–80%
- Stroke:   ~95%+ (imbalanced dataset)

> ⚠️ You must train models before running the Flask app. The app will crash on prediction if `.pkl` files are missing.

---

## STEP 6 — Run the Flask Application

```bash
python app.py
```

Open your browser and go to: **http://127.0.0.1:5000**

---

## Role-Based Access — How It Works

Each doctor is linked to a department in the database.
The system checks their department at login and shows only relevant prediction:

| Department       | Doctor Email            | Can Run Prediction    |
|------------------|-------------------------|-----------------------|
| Cardiology       | heart@hospital.com      | ❤️  Heart Disease    |
| Neurology        | neuro@hospital.com      | 🧠  Stroke           |
| General Medicine | general@hospital.com    | 🩸  Diabetes         |

Doctors from other departments get an **"Access Denied"** page — not an error.

---

## Project Folder Structure

```
AI_powered_HMS/
├── app.py                          ← Flask entry point
├── config.py                       ← DB credentials & secret key
├── requirements.txt                ← pip packages
├── train_all_models.py             ← Run once to train all 3 models
├── HOW_TO_RUN.md                   ← This file
├── SAMPLE_DATA.md                  ← SQL inserts for demo data
├── sql_readme.md                   ← Full CREATE TABLE SQL
│
├── dataset/
│   ├── heart.csv
│   ├── diabetes.csv
│   └── stroke.csv
│
├── ml_pipeline/
│   ├── predict.py                  ← Used by Flask routes
│   ├── train_heart_model.py
│   ├── train_diabetes_model.py
│   └── train_stroke_model.py
│
├── model/                          ← Created after training
│   ├── heart_model.pkl
│   ├── diabetes_model.pkl
│   ├── diabetes_scaler.pkl
│   ├── stroke_model.pkl
│   ├── heart_model_accuracy.txt
│   ├── diabetes_model_accuracy.txt
│   └── stroke_model_accuracy.txt
│
├── database/
│   └── connection.py
│
├── routes/
│   ├── auth_routes.py
│   ├── admin_routes.py
│   ├── doctor_routes.py
│   ├── nurse_routes.py
│   └── patient_routes.py
│
├── static/css/
│   ├── style.css
│   └── dashboard.css
│
└── templates/
    ├── layout/base.html
    ├── common/  (index, login, register)
    ├── admin/   (dashboard, departments, users)
    ├── doctor/  (dashboard, patients, predict_heart/diabetes/stroke)
    ├── nurse/   (dashboard, vitals, records)
    ├── patient/ (dashboard, results)
    └── error/   (unauthorized)
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: flask` | Run `pip install -r requirements.txt` inside venv |
| `mysql.connector.errors.DatabaseError` | Check config.py DB credentials and that MySQL is running |
| `FileNotFoundError: heart_model.pkl` | Run `python train_all_models.py` first |
| Doctor sees "Access Denied" | Check `doctors` table — dept_id must match Cardiology/Neurology/General Medicine |
| Patient has no results | Patient's `user_id` must be in `patients` table; ask admin to add them |
| Nurse can't record vitals | Nurse's `user_id` must be in `nurses` table |
