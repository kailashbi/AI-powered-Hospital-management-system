from flask import request
from server.app.extensions import db
from server.app.models.audit_log import AuditLog

def log_action(user_id, action, entity_type, entity_id=None, details=None):
    try:
        ip = request.remote_addr if request else '127.0.0.1'
        log = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
            ip_address=ip
        )
        db.session.add(log)
        db.session.commit()

        # Stream Kafka Audit Event
        try:
            from server.app.services.kafka_service import kafka_service
            kafka_service.publish_event(
                topic=kafka_service.TOPICS['AUDIT_LOGS'],
                event_type=f"AUDIT_{action}",
                payload=log.to_dict(),
                key=str(user_id)
            )
        except Exception:
            pass
    except Exception as e:

        db.session.rollback()
        print(f"[Audit Log Warning] Failed to log action {action}: {e}")
