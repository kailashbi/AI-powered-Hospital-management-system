from server.app.extensions import db
from server.app.models.notification import Notification

class NotificationService:
    @staticmethod
    def send_notification(user_id: int, title: str, message: str, type_str='General', action_url=None):
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=type_str,
            action_url=action_url,
            is_read=False
        )
        db.session.add(notif)
        db.session.commit()
        return notif.to_dict()

    @staticmethod
    def get_user_notifications(user_id: int):
        notifs = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).limit(30).all()
        return [n.to_dict() for n in notifs]

    @staticmethod
    def mark_as_read(notif_id: int, user_id: int):
        notif = Notification.query.filter_by(id=notif_id, user_id=user_id).first()
        if notif:
            notif.is_read = True
            db.session.commit()
            return True
        return False

    @staticmethod
    def mark_all_read(user_id: int):
        Notification.query.filter_by(user_id=user_id, is_read=False).update({'is_read': True})
        db.session.commit()
        return True
