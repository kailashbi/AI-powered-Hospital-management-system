from flask import Blueprint, render_template, request, redirect, session
from database.connection import get_db_connection

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required():
    return session.get("role_id") == 1


@admin_bp.route("/dashboard")
def dashboard():
    if not admin_required():
        return redirect("/login")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as cnt FROM users")
    users_count = cursor.fetchone()["cnt"]
    cursor.execute("SELECT COUNT(*) as cnt FROM departments")
    dept_count = cursor.fetchone()["cnt"]
    cursor.execute("SELECT COUNT(*) as cnt FROM predictions")
    pred_count = cursor.fetchone()["cnt"]
    cursor.close(); conn.close()
    return render_template("admin/admin_dashboard.html",
                           users_count=users_count, dept_count=dept_count, pred_count=pred_count)


@admin_bp.route("/departments")
def departments():
    if not admin_required():
        return redirect("/login")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM departments")
    departments = cursor.fetchall()
    cursor.close(); conn.close()
    return render_template("admin/manage_departments.html", departments=departments)


@admin_bp.route("/add_department", methods=["POST"])
def add_department():
    if not admin_required():
        return redirect("/login")
    dept_name = request.form["dept_name"]
    description = request.form.get("description", "")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO departments (dept_name, description) VALUES (%s,%s)", (dept_name, description))
    conn.commit()
    cursor.close(); conn.close()
    return redirect("/admin/departments")


@admin_bp.route("/delete_department/<int:id>")
def delete_department(id):
    if not admin_required():
        return redirect("/login")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM departments WHERE dept_id=%s", (id,))
    conn.commit()
    cursor.close(); conn.close()
    return redirect("/admin/departments")


@admin_bp.route("/users")
def users():
    if not admin_required():
        return redirect("/login")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.user_id, u.name, u.email, r.role_name, u.created_at
        FROM users u JOIN roles r ON u.role_id = r.role_id
        ORDER BY u.created_at DESC
    """)
    users_list = cursor.fetchall()
    cursor.close(); conn.close()
    return render_template("admin/manage_users.html", users=users_list)
