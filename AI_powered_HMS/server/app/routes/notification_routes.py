from flask import Blueprint, jsonify
from server.app.models import Notification
from server.app.middleware.auth import token_required
from server.app.services.notification_service import NotificationService

notification_bp = Blueprint('notification_bp', __name__, url_prefix='/api/notifications')

@notification_bp.route('', methods=['GET'])
@token_required
def get_my_notifications(current_user):
    notifs = NotificationService.get_user_notifications(current_user.id)
    return jsonify({'success': True, 'notifications': notifs}), 200

@notification_bp.route('/<int:notif_id>/read', methods=['PATCH'])
@token_required
def mark_as_read(current_user, notif_id):
    success = NotificationService.mark_as_read(notif_id, current_user.id)
    return jsonify({'success': success}), 200

@notification_bp.route('/mark-all-read', methods=['POST'])
@token_required
def mark_all_read(current_user):
    NotificationService.mark_all_read(current_user.id)
    return jsonify({'success': True, 'message': 'All notifications marked as read'}), 200
