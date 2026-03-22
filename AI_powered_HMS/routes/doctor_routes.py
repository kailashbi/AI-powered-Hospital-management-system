from flask import Blueprint, render_template, request, session, redirect
import numpy as np
from database.connection import get_db_connection

doctor_bp = Blueprint("doctor", __name__, url_prefix="/doctor")


def doctor_required():
    return session.get("role_id") == 2


def get_doctor_dept(cursor):
    """Return (doctor_id, dept_name) for logged-in doctor, or (None, None)."""
    cursor.execute("""
        SELECT d.doctor_id, dept.dept_name
        FROM doctors d
        JOIN departments dept ON d.dept_id = dept.dept_id
        WHERE d.user_id = %s
    """, (session["user_id"],))
    row = cursor.fetchone()
    if row:
        return row["doctor_id"], row["dept_name"].strip().lower()
    return None, None


# ─── Dashboard ──────────────────────────────────────────────────────────────
@doctor_bp.route("/dashboard")
def dashboard():
    if not doctor_required():
        return redirect("/login")
    conn   = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT u.name, d.specialization, d.experience, d.phone, dept.dept_name
        FROM users u
        JOIN doctors d    ON u.user_id  = d.user_id
        JOIN departments dept ON d.dept_id = dept.dept_id
        WHERE u.user_id = %s
    """, (session["user_id"],))
    doctor = cursor.fetchone()

    cursor.execute("""
        SELECT COUNT(*) AS total_predictions
        FROM predictions p
        JOIN doctors d ON p.doctor_id = d.doctor_id
        WHERE d.user_id = %s
    """, (session["user_id"],))
    stats = cursor.fetchone()
    cursor.close(); conn.close()
    return render_template("doctor/doctor_dashboard.html", doctor=doctor, stats=stats)


# ─── Patient list ───────────────────────────────────────────────────────────
@doctor_bp.route("/patients")
def patients():
    if not doctor_required():
        return redirect("/login")
    conn   = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT pat.patient_id, u.name, pat.age, pat.gender, pat.phone, pat.address
        FROM patients pat
        JOIN users u ON pat.user_id = u.user_id
        ORDER BY pat.patient_id DESC
    """)
    patient_list = cursor.fetchall()
    cursor.close(); conn.close()
    return render_template("doctor/patients.html", patients=patient_list)


# ─── Heart Prediction ───────────────────────────────────────────────────────
@doctor_bp.route("/predict_heart", methods=["GET", "POST"])
def predict_heart():
    if not doctor_required():
        return redirect("/login")
    conn   = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    doctor_id, dept_name = get_doctor_dept(cursor)
    if dept_name != "cardiology":
        cursor.close(); conn.close()
        return render_template("error/unauthorized.html",
            message="Only Cardiology doctors can run Heart Disease prediction.")

    result = None
    if request.method == "POST":
        from ml_pipeline.predict import predict_heart as _pred
        try:
            age      = float(request.form["age"])
            sex      = float(request.form["sex"])
            cp       = float(request.form["cp"])
            trestbps = float(request.form["trestbps"])
            chol     = float(request.form["chol"])
            fbs      = float(request.form.get("fbs", 0))
            restecg  = float(request.form.get("restecg", 0))
            thalach  = float(request.form["thalach"])
            exang    = float(request.form.get("exang", 0))
            oldpeak  = float(request.form["oldpeak"])
            slope    = float(request.form.get("slope", 0))
            ca       = float(request.form.get("ca", 0))
            thal     = float(request.form.get("thal", 0))

            # ── FIXED: pass named arguments, not numpy array ──────────
            pred, prob = _pred(
                age=age, sex=sex, cp=cp, trestbps=trestbps,
                chol=chol, fbs=fbs, restecg=restecg, thalch=thalach,
                exang=exang, oldpeak=oldpeak, slope=slope, ca=ca, thal=thal
            )

            label      = "High Risk" if pred == 1 else "Low Risk"
            patient_id = int(request.form.get("patient_id", 0))

            if doctor_id and patient_id:
                cursor.execute("""
                    INSERT INTO predictions
                      (patient_id, doctor_id, disease_type, prediction_result, probability)
                    VALUES (%s, %s, 'heart', %s, %s)
                """, (patient_id, doctor_id, label, prob))
                pred_id = cursor.lastrowid
                cursor.execute("""
                    INSERT INTO prediction_inputs
                      (prediction_id, age, sex, cp, trestbps, chol, thalach, oldpeak)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (pred_id, int(age), int(sex), int(cp),
                      int(trestbps), int(chol), int(thalach), oldpeak))
                conn.commit()

            result = {"label": label, "probability": round(prob*100, 2),
                      "disease": "Heart Disease", "risk": pred == 1}
        except Exception as e:
            result = {"error": str(e)}

    cursor.execute("""
        SELECT pat.patient_id, u.name
        FROM patients pat JOIN users u ON pat.user_id = u.user_id
        ORDER BY u.name
    """)
    patients = cursor.fetchall()
    cursor.close(); conn.close()
    return render_template("doctor/predict_heart.html", result=result, patients=patients)


# ─── Diabetes Prediction ────────────────────────────────────────────────────
@doctor_bp.route("/predict_diabetes", methods=["GET", "POST"])
def predict_diabetes():
    if not doctor_required():
        return redirect("/login")
    conn   = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    doctor_id, dept_name = get_doctor_dept(cursor)
    if dept_name != "general medicine":
        cursor.close(); conn.close()
        return render_template("error/unauthorized.html",
            message="Only General Medicine doctors can run Diabetes prediction.")

    result = None
    if request.method == "POST":
        from ml_pipeline.predict import predict_diabetes as _pred
        try:
            pregnancies = float(request.form.get("pregnancies", 0))
            glucose     = float(request.form["glucose"])
            bp_val      = float(request.form["blood_pressure"])
            skin_thick  = float(request.form.get("skin_thickness", 0))
            insulin     = float(request.form.get("insulin", 0))
            bmi         = float(request.form["bmi"])
            dpf         = float(request.form.get("diabetes_pedigree", 0))
            age         = float(request.form["age"])

            data       = np.array([[pregnancies, glucose, bp_val, skin_thick, insulin, bmi, dpf, age]])
            pred, prob = _pred(data)
            label      = "Diabetes Detected" if pred == 1 else "No Diabetes"
            patient_id = int(request.form.get("patient_id", 0))

            if doctor_id and patient_id:
                cursor.execute("""
                    INSERT INTO predictions
                      (patient_id, doctor_id, disease_type, prediction_result, probability)
                    VALUES (%s, %s, 'diabetes', %s, %s)
                """, (patient_id, doctor_id, label, prob))
                conn.commit()

            result = {"label": label, "probability": round(prob*100, 2), "disease": "Diabetes",
                      "risk": pred == 1}
        except Exception as e:
            result = {"error": str(e)}

    cursor.execute("""
        SELECT pat.patient_id, u.name
        FROM patients pat JOIN users u ON pat.user_id = u.user_id
        ORDER BY u.name
    """)
    patients = cursor.fetchall()
    cursor.close(); conn.close()
    return render_template("doctor/predict_diabetes.html", result=result, patients=patients)


# ─── Stroke Prediction ──────────────────────────────────────────────────────
@doctor_bp.route("/predict_stroke", methods=["GET", "POST"])
def predict_stroke():
    if not doctor_required():
        return redirect("/login")
    conn   = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    doctor_id, dept_name = get_doctor_dept(cursor)
    if dept_name != "neurology":
        cursor.close(); conn.close()
        return render_template("error/unauthorized.html",
            message="Only Neurology doctors can run Stroke prediction.")

    result = None
    if request.method == "POST":
        from ml_pipeline.predict import predict_stroke as _pred
        try:
            gender         = float(request.form.get("gender", 1))
            age            = float(request.form["age"])
            hypertension   = float(request.form.get("hypertension", 0))
            heart_disease  = float(request.form.get("heart_disease", 0))
            ever_married   = float(request.form.get("ever_married", 1))
            work_type      = float(request.form.get("work_type", 3))
            residence_type = float(request.form.get("residence_type", 1))
            avg_glucose    = float(request.form["avg_glucose"])
            bmi            = float(request.form["bmi"])
            smoking_status = float(request.form.get("smoking_status", 1))

            data       = np.array([[gender, age, hypertension, heart_disease, ever_married,
                                    work_type, residence_type, avg_glucose, bmi, smoking_status]])
            pred, prob = _pred(data)
            label      = "Stroke Risk" if pred == 1 else "Low Risk"
            patient_id = int(request.form.get("patient_id", 0))

            if doctor_id and patient_id:
                cursor.execute("""
                    INSERT INTO predictions
                      (patient_id, doctor_id, disease_type, prediction_result, probability)
                    VALUES (%s, %s, 'stroke', %s, %s)
                """, (patient_id, doctor_id, label, prob))
                conn.commit()

            result = {"label": label, "probability": round(prob*100, 2), "disease": "Stroke",
                      "risk": pred == 1}
        except Exception as e:
            result = {"error": str(e)}

    cursor.execute("""
        SELECT pat.patient_id, u.name
        FROM patients pat JOIN users u ON pat.user_id = u.user_id
        ORDER BY u.name
    """)
    patients = cursor.fetchall()
    cursor.close(); conn.close()
    return render_template("doctor/predict_stroke.html", result=result, patients=patients)
