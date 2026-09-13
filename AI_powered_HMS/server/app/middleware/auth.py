import jwt
from functools import wraps
from flask import request, jsonify, current_app
from server.app.models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            parts = auth_header.split(' ')
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
            else:
                token = auth_header

        if not token:
            return jsonify({'success': False, 'message': 'Authentication token is missing'}), 401

        try:
            secret = current_app.config.get('JWT_SECRET_KEY', 'kaire-jwt-secure-token-2026')
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            user_id = payload.get('sub') or payload.get('user_id')
            current_user = User.query.get(user_id)
            if not current_user or not current_user.is_active:
                return jsonify({'success': False, 'message': 'User account not found or deactivated'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'message': 'Session token has expired. Please log in again.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'message': 'Invalid authentication token'}), 401
        except Exception as e:
            return jsonify({'success': False, 'message': f'Auth token verification failed: {str(e)}'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

def role_required(allowed_roles):
    """
    Decorator for role-based access control.
    e.g. @role_required(['admin', 'doctor'])
    """
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]

    def decorator(f):
        @wraps(f)
        @token_required
        def wrapper(current_user, *args, **kwargs):
            if current_user.role not in allowed_roles:
                return jsonify({
                    'success': False,
                    'message': f'Access forbidden. Role required: {", ".join(allowed_roles)}. Your role: {current_user.role}'
                }), 403
            return f(current_user, *args, **kwargs)
        return wrapper
    return decorator
