from flask import Blueprint, render_template, session, redirect
from database.connection import get_db_connection

patient_bp = Blueprint("patient", __name__, url_prefix="/patient")


def patient_required():
    return session.get("role_id") == 4


@patient_bp.route("/dashboard")
def dashboard():
    if not patient_required():
        return redirect("/login")
    conn   = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Try to load patient profile; may not exist if admin hasn't added it yet
    cursor.execute("""
        SELECT pat.patient_id, pat.age, pat.gender, pat.phone, pat.address
        FROM patients pat
        WHERE pat.user_id = %s
    """, (session["user_id"],))
    patient = cursor.fetchone()

    pred_count = 0
    if patient:
        cursor.execute("SELECT COUNT(*) AS cnt FROM predictions WHERE patient_id = %s",
                       (patient["patient_id"],))
        pred_count = cursor.fetchone()["cnt"]

    cursor.close(); conn.close()
    return render_template("patient/patient_dashboard.html",
                           patient=patient, pred_count=pred_count)


@patient_bp.route("/results")
def results():
    if not patient_required():
        return redirect("/login")
    conn   = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT patient_id FROM patients WHERE user_id = %s", (session["user_id"],))
    pat = cursor.fetchone()
    predictions = []
    if pat:
        cursor.execute("""
            SELECT pr.disease_type, pr.prediction_result,
                   pr.probability, pr.created_at,
                   u.name  AS doctor_name,
                   dept.dept_name
            FROM predictions pr
            LEFT JOIN doctors  d    ON pr.doctor_id  = d.doctor_id
            LEFT JOIN users    u    ON d.user_id      = u.user_id
            LEFT JOIN departments dept ON d.dept_id   = dept.dept_id
            WHERE pr.patient_id = %s
            ORDER BY pr.created_at DESC
        """, (pat["patient_id"],))
        predictions = cursor.fetchall()
    cursor.close(); conn.close()
    return render_template("patient/patient_result_view.html", predictions=predictions)
