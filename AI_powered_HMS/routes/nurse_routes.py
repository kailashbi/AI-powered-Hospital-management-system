from flask import Blueprint, render_template, request, redirect, session
from database.connection import get_db_connection

nurse_bp = Blueprint("nurse", __name__, url_prefix="/nurse")


def nurse_required():
    return session.get("role_id") == 3


@nurse_bp.route("/dashboard")
def dashboard():
    if not nurse_required():
        return redirect("/login")
    conn   = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as cnt FROM vitals")
    vitals_count  = cursor.fetchone()["cnt"]
    cursor.execute("SELECT COUNT(*) as cnt FROM patients")
    patient_count = cursor.fetchone()["cnt"]
    # Nurse info
    cursor.execute("""
        SELECT n.nurse_id, d.dept_name
        FROM nurses n
        JOIN departments d ON n.dept_id = d.dept_id
        WHERE n.user_id = %s
    """, (session["user_id"],))
    nurse_info = cursor.fetchone()
    cursor.close(); conn.close()
    return render_template("nurse/nurse_dashboard.html",
                           vitals_count=vitals_count,
                           patient_count=patient_count,
                           nurse_info=nurse_info)


@nurse_bp.route("/vitals", methods=["GET", "POST"])
def vitals():
    if not nurse_required():
        return redirect("/login")
    success = False
    conn   = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        patient_id = int(request.form["patient_id"])
        bp         = request.form["bp"]        or None
        chol       = request.form["chol"]      or None
        glucose    = request.form["glucose"]   or None
        heart_rate = request.form.get("heart_rate") or None
        bmi        = request.form.get("bmi")   or None

        # Get nurse_id for recorded_by (matches vitals.recorded_by → nurses.nurse_id)
        cursor.execute("SELECT nurse_id FROM nurses WHERE user_id = %s", (session["user_id"],))
        nurse_row   = cursor.fetchone()
        recorded_by = nurse_row["nurse_id"] if nurse_row else None

        cursor.execute("""
            INSERT INTO vitals
              (patient_id, blood_pressure, cholesterol, glucose, heart_rate, bmi, recorded_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (patient_id, bp, chol, glucose, heart_rate, bmi, recorded_by))
        conn.commit()
        success = True

    cursor.execute("""
        SELECT pat.patient_id, u.name
        FROM patients pat
        JOIN users u ON pat.user_id = u.user_id
        ORDER BY u.name
    """)
    patients = cursor.fetchall()
    cursor.close(); conn.close()
    return render_template("nurse/patient_vitals.html", patients=patients, success=success)


@nurse_bp.route("/records")
def records():
    if not nurse_required():
        return redirect("/login")
    conn   = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.name AS patient_name,
               v.blood_pressure, v.cholesterol, v.glucose,
               v.heart_rate, v.bmi, v.recorded_at,
               un.name AS recorded_by_name
        FROM vitals v
        JOIN patients p  ON v.patient_id  = p.patient_id
        JOIN users u     ON p.user_id     = u.user_id
        LEFT JOIN nurses n  ON v.recorded_by = n.nurse_id
        LEFT JOIN users un  ON n.user_id     = un.user_id
        ORDER BY v.recorded_at DESC
    """)
    records = cursor.fetchall()
    cursor.close(); conn.close()
    return render_template("nurse/patient_records.html", records=records)
