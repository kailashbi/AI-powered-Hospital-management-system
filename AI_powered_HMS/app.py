from flask import Flask
from config import SECRET_KEY

from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.doctor_routes import doctor_bp
from routes.nurse_routes import nurse_bp
from routes.patient_routes import patient_bp

app = Flask(__name__)

app.secret_key = SECRET_KEY

# Register Blueprints

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(nurse_bp)
app.register_blueprint(patient_bp)

if __name__ == "__main__":
    app.run(debug=True)