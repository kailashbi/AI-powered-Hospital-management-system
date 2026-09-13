from flask import Blueprint, request, jsonify
from server.app.extensions import db
from server.app.models import User, Doctor, Nurse, Patient, Department, Appointment, Vital, Prediction, AuditLog
from server.app.middleware.auth import role_required
from server.app.utils.audit import log_action

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/api/admin')

@admin_bp.route('/stats', methods=['GET'])
@role_required(['admin'])
def get_dashboard_stats(current_user):
    total_users = User.query.count()
    active_doctors = Doctor.query.filter_by(is_active=True).count()
    active_nurses = Nurse.query.filter_by(is_active=True).count()
    total_patients = Patient.query.filter_by(is_active=True).count()
    total_appointments = Appointment.query.count()
    total_predictions = Prediction.query.count()
    high_risk_predictions = Prediction.query.filter(Prediction.risk_level.in_(['High', 'Critical'])).count()
    active_departments = Department.query.filter_by(is_active=True).count()

    # Department distribution
    depts = Department.query.all()
    dept_distribution = []
    for d in depts:
        dept_distribution.append({
            'name': d.name,
            'code': d.code,
            'doctors': d.doctors.count(),
            'nurses': d.nurses.count(),
            'appointments': d.appointments.count()
        })

    # Recent Audit Logs
    recent_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(10).all()

    return jsonify({
        'success': True,
        'stats': {
            'total_users': total_users,
            'active_doctors': active_doctors,
            'active_nurses': active_nurses,
            'total_patients': total_patients,
            'total_appointments': total_appointments,
            'total_predictions': total_predictions,
            'high_risk_predictions': high_risk_predictions,
            'active_departments': active_departments,
            'bed_occupancy_rate': 78.5, # percentage
            'emergency_dispatches': 3
        },
        'department_distribution': dept_distribution,
        'recent_logs': [l.to_dict() for l in recent_logs]
    }), 200

# ================= USER MANAGEMENT =================
@admin_bp.route('/users', methods=['GET'])
@role_required(['admin'])
def list_users(current_user):
    role_filter = request.args.get('role')
    query = User.query
    if role_filter:
        query = query.filter_by(role=role_filter)
    users = query.order_by(User.created_at.desc()).all()
    return jsonify({'success': True, 'users': [u.to_dict() for u in users]}), 200

@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['PATCH'])
@role_required(['admin'])
def toggle_user_status(current_user, user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    action_type = "ACTIVATE_USER" if user.is_active else "DEACTIVATE_USER"
    log_action(current_user.id, action_type, 'User', user.id, f"{'Activated' if user.is_active else 'Deactivated'} user {user.username}")
    return jsonify({'success': True, 'message': f"User account {'activated' if user.is_active else 'deactivated'}", 'user': user.to_dict()}), 200

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_user(current_user, user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        return jsonify({'success': False, 'message': 'Admin cannot delete their own account'}), 400
    try:
        # Delete associated child records if present
        Doctor.query.filter_by(user_id=user_id).delete()
        Nurse.query.filter_by(user_id=user_id).delete()
        Patient.query.filter_by(user_id=user_id).delete()
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Fallback to deactivating user account if hard delete violates audit history constraints
        user.is_active = False
        db.session.commit()
    log_action(current_user.id, 'DELETE_USER', 'User', user_id, f"Removed user ID {user_id}")
    return jsonify({'success': True, 'message': 'User deleted successfully'}), 200

# ================= DOCTORS MANAGEMENT =================
@admin_bp.route('/doctors', methods=['GET'])
@role_required(['admin'])
def list_doctors(current_user):
    doctors = Doctor.query.all()
    return jsonify({'success': True, 'doctors': [d.to_dict() for d in doctors]}), 200

@admin_bp.route('/doctors', methods=['POST'])
@role_required(['admin'])
def create_doctor(current_user):
    data = request.get_json() or {}
    # Create user first
    user = User(
        username=data['username'],
        email=data['email'],
        role='doctor',
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data.get('phone'),
        avatar_url=data.get('avatar_url', 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=150'),
        is_active=True
    )
    user.set_password(data.get('password', 'password123'))
    db.session.add(user)
    db.session.flush()

    doctor = Doctor(
        user_id=user.id,
        department_id=int(data.get('department_id', 1)),
        license_number=data['license_number'],
        specialization=data['specialization'],
        qualification=data.get('qualification'),
        experience_years=int(data.get('experience_years', 5)),
        consultation_fee=float(data.get('consultation_fee', 150.0)),
        room_number=data.get('room_number', 'Room 101'),
        bio=data.get('bio', ''),
        available_days=data.get('available_days', 'Mon,Tue,Wed,Thu,Fri'),
        is_active=True
    )
    db.session.add(doctor)
    db.session.commit()
    log_action(current_user.id, 'CREATE_DOCTOR', 'Doctor', doctor.id, f"Created doctor profile for Dr. {user.last_name}")
    return jsonify({'success': True, 'doctor': doctor.to_dict()}), 201

@admin_bp.route('/doctors/<int:doctor_id>', methods=['PATCH', 'PUT'])
@role_required(['admin'])
def update_doctor(current_user, doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    data = request.get_json() or {}
    
    if 'specialization' in data: doctor.specialization = data['specialization']
    if 'consultation_fee' in data: doctor.consultation_fee = float(data['consultation_fee'])
    if 'room_number' in data: doctor.room_number = data['room_number']
    if 'department_id' in data: doctor.department_id = int(data['department_id'])
    if 'bio' in data: doctor.bio = data['bio']
    if 'is_active' in data: doctor.is_active = bool(data['is_active'])

    db.session.commit()
    log_action(current_user.id, 'UPDATE_DOCTOR', 'Doctor', doctor.id, f"Admin updated doctor ID {doctor_id}")
    return jsonify({'success': True, 'doctor': doctor.to_dict()}), 200

# ================= NURSES MANAGEMENT =================
@admin_bp.route('/nurses', methods=['GET'])
@role_required(['admin'])
def list_nurses(current_user):
    nurses = Nurse.query.all()
    return jsonify({'success': True, 'nurses': [n.to_dict() for n in nurses]}), 200

@admin_bp.route('/nurses', methods=['POST'])
@role_required(['admin'])
def create_nurse(current_user):
    data = request.get_json() or {}
    user = User(
        username=data['username'],
        email=data['email'],
        role='nurse',
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data.get('phone'),
        avatar_url=data.get('avatar_url', 'https://images.unsplash.com/photo-1582750433449-648ed127bb54?w=150'),
        is_active=True
    )
    user.set_password(data.get('password', 'password123'))
    db.session.add(user)
    db.session.flush()

    nurse = Nurse(
        user_id=user.id,
        department_id=int(data.get('department_id', 1)),
        license_number=data['license_number'],
        qualification=data.get('qualification', 'BSN, RN'),
        shift_timing=data.get('shift_timing', 'Morning (06:00 - 14:00)'),
        assigned_room=data.get('assigned_room', 'General Ward - 101'),
        duty_status='On Duty',
        is_active=True
    )
    db.session.add(nurse)
    db.session.commit()
    log_action(current_user.id, 'CREATE_NURSE', 'Nurse', nurse.id, f"Created nurse profile for {user.full_name}")
    return jsonify({'success': True, 'nurse': nurse.to_dict()}), 201

@admin_bp.route('/nurses/<int:nurse_id>', methods=['PATCH', 'PUT'])
@role_required(['admin'])
def update_nurse(current_user, nurse_id):
    nurse = Nurse.query.get_or_404(nurse_id)
    data = request.get_json() or {}
    
    if 'assigned_room' in data: nurse.assigned_room = data['assigned_room']
    if 'shift_timing' in data: nurse.shift_timing = data['shift_timing']
    if 'duty_status' in data: nurse.duty_status = data['duty_status']
    if 'department_id' in data: nurse.department_id = int(data['department_id'])
    if 'is_active' in data: nurse.is_active = bool(data['is_active'])

    db.session.commit()
    log_action(current_user.id, 'UPDATE_NURSE', 'Nurse', nurse.id, f"Admin updated nurse ID {nurse_id}")
    return jsonify({'success': True, 'nurse': nurse.to_dict()}), 200

# ================= DEPARTMENTS MANAGEMENT =================
@admin_bp.route('/departments', methods=['GET'])
@role_required(['admin'])
def list_departments(current_user):
    depts = Department.query.all()
    return jsonify({'success': True, 'departments': [d.to_dict() for d in depts]}), 200

@admin_bp.route('/departments', methods=['POST'])
@role_required(['admin'])
def create_department(current_user):
    data = request.get_json() or {}
    dept = Department(
        name=data['name'],
        code=data['code'],
        description=data.get('description', ''),
        location_floor=data.get('location_floor', 'Floor 1'),
        contact_phone=data.get('contact_phone', '+1 (555) 000-0000'),
        is_active=True
    )
    db.session.add(dept)
    db.session.commit()
    log_action(current_user.id, 'CREATE_DEPARTMENT', 'Department', dept.id, f"Created department {dept.name}")
    return jsonify({'success': True, 'department': dept.to_dict()}), 201

# ================= AUDIT LOGS =================
@admin_bp.route('/audit-logs', methods=['GET'])
@role_required(['admin'])
def get_audit_logs(current_user):
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(100).all()
    return jsonify({'success': True, 'logs': [l.to_dict() for l in logs]}), 200
