from flask import Blueprint, jsonify, request
from server.app.services.kafka_service import kafka_service
from server.app.middleware.auth import token_required

kafka_bp = Blueprint('kafka_bp', __name__, url_prefix='/api/kafka')

@kafka_bp.route('/status', methods=['GET'])
def get_kafka_status():
    """
    Get Kafka Cluster & Event Streaming Status
    ---
    tags:
      - Kafka Architecture
    responses:
      200:
        description: Returns cluster connection metrics and active topics
    """
    status_data = kafka_service.get_status()
    return jsonify({
        'status': 'success',
        'kafka': status_data
    }), 200

@kafka_bp.route('/events', methods=['GET'])
def get_kafka_events():
    """
    Get Live Event Log Buffer
    ---
    tags:
      - Kafka Architecture
    parameters:
      - name: topic
        in: query
        type: string
        required: false
      - name: limit
        in: query
        type: integer
        required: false
    responses:
      200:
        description: List of streaming event payloads
    """
    topic = request.args.get('topic')
    limit = int(request.args.get('limit', 50))
    events = kafka_service.get_recent_events(topic=topic, limit=limit)
    return jsonify({
        'status': 'success',
        'count': len(events),
        'events': events
    }), 200

@kafka_bp.route('/publish', methods=['POST'])
@token_required
def publish_test_event(current_user):
    """
    Publish Event to Kafka (Test / Demo Trigger)
    ---
    tags:
      - Kafka Architecture
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            topic:
              type: string
            event_type:
              type: string
            payload:
              type: object
    responses:
      201:
        description: Event published successfully
    """
    data = request.get_json() or {}
    topic = data.get('topic', kafka_service.TOPICS['VITALS_STREAM'])
    event_type = data.get('event_type', 'MANUAL_TEST_EVENT')
    payload = data.get('payload', {'triggered_by': current_user.full_name, 'role': current_user.role})

    event = kafka_service.publish_event(topic, event_type, payload, key=str(current_user.id))
    return jsonify({
        'status': 'success',
        'message': 'Event published to Kafka stream successfully',
        'event': event
    }), 201
