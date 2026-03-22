from flask import Blueprint, render_template, request, redirect, session, flash
from database.connection import get_db_connection

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    return render_template("common/index.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email    = request.form["email"]
        password = request.form["password"]

        conn   = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close(); conn.close()

        if user and user["password"] == password:
            session["user_id"] = user["user_id"]
            session["role_id"] = user["role_id"]
            session["name"]    = user["name"]

            if   user["role_id"] == 1: return redirect("/admin/dashboard")
            elif user["role_id"] == 2: return redirect("/doctor/dashboard")
            elif user["role_id"] == 3: return redirect("/nurse/dashboard")
            else:                      return redirect("/patient/dashboard")
        else:
            error = "Invalid email or password."

    return render_template("common/login.html", error=error)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name     = request.form["name"]
        email    = request.form["email"]
        password = request.form["password"]

        conn   = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password, role_id) VALUES (%s,%s,%s,4)",
            (name, email, password)
        )
        conn.commit()
        cursor.close(); conn.close()
        return redirect("/login")

    return render_template("common/register.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
