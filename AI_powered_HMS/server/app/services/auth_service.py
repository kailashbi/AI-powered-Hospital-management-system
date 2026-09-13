import jwt
from datetime import datetime, timedelta
from flask import current_app
from server.app.extensions import db
from server.app.models.user import User

class AuthService:
    @staticmethod
    def generate_token(user: User):
        expires_hours = current_app.config.get('JWT_EXPIRES_HOURS', 12)
        payload = {
            'sub': user.id,
            'user_id': user.id,
            'email': user.email,
            'role': user.role,
            'name': user.full_name,
            'exp': datetime.utcnow() + timedelta(hours=int(expires_hours)),
            'iat': datetime.utcnow()
        }
        secret = current_app.config.get('JWT_SECRET_KEY', 'kaire-jwt-secure-token-2026')
        return jwt.encode(payload, secret, algorithm='HS256')

    @staticmethod
    def authenticate(email_or_username, password):
        user = User.query.filter(
            (User.email == email_or_username.strip()) |
            (User.username == email_or_username.strip())
        ).first()

        if not user or not user.is_active:
            return None, 'Account does not exist or is inactive'

        if not user.check_password(password):
            return None, 'Invalid credentials'

        token = AuthService.generate_token(user)
        return {
            'token': token,
            'user': user.to_dict()
        }, None
