from flask import Blueprint, request, jsonify
from server.app.extensions import db
from server.app.models.user import User
from server.app.models.patient import Patient
from server.app.services.auth_service import AuthService
from server.app.middleware.auth import token_required
from server.app.utils.audit import log_action

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email_or_user = data.get('email') or data.get('username')
    password = data.get('password')

    if not email_or_user or not password:
        return jsonify({'success': False, 'message': 'Email/username and password are required'}), 400

    auth_data, err = AuthService.authenticate(email_or_user, password)
    if err:
        return jsonify({'success': False, 'message': err}), 401

    log_action(auth_data['user']['id'], 'USER_LOGIN', 'User', auth_data['user']['id'], f"User {auth_data['user']['username']} logged in successfully")
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'token': auth_data['token'],
        'user': auth_data['user']
    }), 200

@auth_bp.route('/quick-login', methods=['POST'])
def quick_login():
    """
    Fast demo login for reviewers and testers to easily toggle between roles and personas.
    Accepts role/persona: 'admin', 'doctor', 'doctor_sarah', 'doctor_alex', 'doctor_elena',
    'nurse', 'nurse_emily', 'nurse_marcus', 'patient', 'patient_john', 'patient_maria', 'patient_robert', 'patient_aisha'
    """
    data = request.get_json() or {}
    role = data.get('role', 'admin').lower()
    
    persona_email_map = {
        'admin': 'admin@kairehealth.com',
        'doctor': 'dr.sarah@kairehealth.com',
        'doctor_sarah': 'dr.sarah@kairehealth.com',
        'doctor_alex': 'dr.alex@kairehealth.com',
        'doctor_elena': 'dr.elena@kairehealth.com',
        'nurse': 'nurse.emily@kairehealth.com',
        'nurse_emily': 'nurse.emily@kairehealth.com',
        'nurse_marcus': 'nurse.marcus@kairehealth.com',
        'patient': 'john.doe@gmail.com',
        'patient_john': 'john.doe@gmail.com',
        'patient_maria': 'maria.garcia@gmail.com',
        'patient_robert': 'robert.chen@gmail.com',
        'patient_aisha': 'aisha.patel@gmail.com'
    }
    
    email = persona_email_map.get(role, 'admin@kairehealth.com')
    user = User.query.filter_by(email=email).first()
    if not user:
        # Fallback to role search
        cleaned_role = role.split('_')[0]
        user = User.query.filter_by(role=cleaned_role).first()

    if not user:
        return jsonify({'success': False, 'message': f'Demo account for {role} not found in database'}), 404

    token = AuthService.generate_token(user)
    return jsonify({
        'success': True,
        'message': f'Switched to {user.full_name} ({user.role.capitalize()}) mode',
        'token': token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Public self-registration is STRICTLY for Patients.
    Doctors, Nurses, and Administrators are provisioned and credentialed exclusively by the Administrator.
    """
    data = request.get_json() or {}
    required = ['username', 'email', 'password', 'first_name', 'last_name']
    for r in required:
        if not data.get(r):
            return jsonify({'success': False, 'message': f'Missing field: {r}'}), 400

    if User.query.filter_by(email=data['email'].strip().lower()).first():
        return jsonify({'success': False, 'message': 'Email is already registered'}), 409

    if User.query.filter_by(username=data['username'].strip()).first():
        return jsonify({'success': False, 'message': 'Username is already taken'}), 409

    # Strictly enforce patient role for public registrations
    user = User(
        username=data['username'].strip(),
        email=data['email'].strip().lower(),
        role='patient', # Enforce patient role only
        first_name=data['first_name'].strip(),
        last_name=data['last_name'].strip(),
        phone=data.get('phone'),
        avatar_url=data.get('avatar_url', 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150'),
        is_active=True
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.flush()

    # Create linked Patient EHR profile
    import uuid
    patient = Patient(
        user_id=user.id,
        patient_code=f"PAT-{uuid.uuid4().hex[:6].upper()}",
        date_of_birth=data.get('date_of_birth', '1995-01-01'),
        gender=data.get('gender', 'Other'),
        blood_group=data.get('blood_group', 'O+'),
        city=data.get('city', 'New York'),
        is_active=True
    )
    db.session.add(patient)
    db.session.commit()

    token = AuthService.generate_token(user)
    log_action(user.id, 'PATIENT_REGISTER', 'User', user.id, f"Patient {user.full_name} registered successfully")

    return jsonify({
        'success': True,
        'message': 'Patient account registered successfully. You can now log in.',
        'token': token,
        'user': user.to_dict()
    }), 201

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    user_dict = current_user.to_dict()
    if current_user.role == 'doctor' and current_user.doctor_profile:
        user_dict['doctor_profile'] = current_user.doctor_profile.to_dict()
    elif current_user.role == 'nurse' and current_user.nurse_profile:
        user_dict['nurse_profile'] = current_user.nurse_profile.to_dict()
    elif current_user.role == 'patient' and current_user.patient_profile:
        user_dict['patient_profile'] = current_user.patient_profile.to_dict()
    return jsonify({'success': True, 'user': user_dict}), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json() or {}
    email = data.get('email')
    if not email:
        return jsonify({'success': False, 'message': 'Email is required'}), 400
    user = User.query.filter_by(email=email.strip().lower()).first()
    # Return friendly confirmation regardless of user existence for privacy
    return jsonify({
        'success': True,
        'message': 'If an account exists with that email, password reset instructions have been sent.'
    }), 200
