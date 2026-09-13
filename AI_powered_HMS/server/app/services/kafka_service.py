import os
import json
import time
import uuid
import threading
from datetime import datetime

# Safe import for Kafka Producer & Consumer
KAFKA_AVAILABLE = False
try:
    from kafka import KafkaProducer, KafkaConsumer
    from kafka.errors import KafkaError
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False


class KAIreKafkaService:
    """
    Enterprise Event Streaming Service using Apache Kafka for KAIre Health HMS.
    Features real-time vitals telemetry, emergency alert dispatching, AI risk streaming,
    and automatic fallback to an in-memory event bus when Kafka is offline or unconfigured.
    """
    
    TOPICS = {
        'VITALS_STREAM': 'kaire-vitals-stream',
        'EMERGENCY_ALERTS': 'kaire-emergency-alerts',
        'ML_PREDICTIONS': 'kaire-ml-predictions',
        'APPOINTMENTS': 'kaire-appointments',
        'NOTIFICATIONS': 'kaire-notifications',
        'AUDIT_LOGS': 'kaire-audit-logs'
    }

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(KAIreKafkaService, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self.enabled = os.environ.get('ENABLE_KAFKA', 'true').lower() in ['true', '1', 'yes']
        self.bootstrap_servers = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.security_protocol = os.environ.get('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT')
        self.sasl_mechanism = os.environ.get('KAFKA_SASL_MECHANISM', 'PLAIN')
        self.sasl_username = os.environ.get('KAFKA_SASL_USERNAME', '')
        self.sasl_password = os.environ.get('KAFKA_SASL_PASSWORD', '')

        self.producer = None
        self.is_connected = False
        self.metrics = {
            'total_events_published': 0,
            'topic_counts': {t: 0 for t in self.TOPICS.values()},
            'emergency_alerts_triggered': 0,
            'mode': 'Offline / In-Memory Fallback'
        }
        self.in_memory_events = []
        self.max_memory_events = 100

        if self.enabled and KAFKA_AVAILABLE:
            self._init_producer()
        else:
            print("[Kafka Service] Running in Graceful Fallback Mode (In-Memory Event Bus enabled)")

        # Start background consumer thread for audit & emergency processing
        self._start_consumer_thread()

    def _init_producer(self):
        try:
            kafka_config = {
                'bootstrap_servers': [s.strip() for s in self.bootstrap_servers.split(',')],
                'value_serializer': lambda v: json.dumps(v).encode('utf-8'),
                'key_serializer': lambda k: str(k).encode('utf-8') if k else None,
                'request_timeout_ms': 5000,
                'max_block_ms': 3000,
                'retries': 2
            }

            if self.security_protocol in ['SASL_PLAINTEXT', 'SASL_SSL']:
                kafka_config['security_protocol'] = self.security_protocol
                kafka_config['sasl_mechanism'] = self.sasl_mechanism
                kafka_config['sasl_plain_username'] = self.sasl_username
                kafka_config['sasl_plain_password'] = self.sasl_password

            self.producer = KafkaProducer(**kafka_config)
            self.is_connected = True
            self.metrics['mode'] = f'Connected to Kafka Cluster ({self.bootstrap_servers})'
            print(f"[✓ Kafka Producer] Successfully connected to Kafka brokers: {self.bootstrap_servers}")

        except Exception as e:
            self.producer = None
            self.is_connected = False
            self.metrics['mode'] = f'Fallback (Broker Connection Failed: {str(e)[:60]})'
            print(f"[Kafka Warning] Could not connect to Kafka brokers ({self.bootstrap_servers}). Using fallback event bus: {e}")

    def publish_event(self, topic: str, event_type: str, payload: dict, key: str = None) -> dict:
        """
        Publishes an event to a Kafka topic.
        Falls back smoothly to in-memory event bus if Kafka broker is unavailable.
        """
        event_id = f"evt_{uuid.uuid4().hex[:10]}"
        timestamp = datetime.utcnow().isoformat() + 'Z'

        formatted_payload = {
            'event_id': event_id,
            'event_type': event_type,
            'topic': topic,
            'timestamp': timestamp,
            'payload': payload
        }

        # Update metrics
        self.metrics['total_events_published'] += 1
        if topic in self.metrics['topic_counts']:
            self.metrics['topic_counts'][topic] += 1
        else:
            self.metrics['topic_counts'][topic] = 1

        if topic == self.TOPICS['EMERGENCY_ALERTS']:
            self.metrics['emergency_alerts_triggered'] += 1

        # Store in memory buffer for live UI monitoring
        self.in_memory_events.insert(0, formatted_payload)
        if len(self.in_memory_events) > self.max_memory_events:
            self.in_memory_events.pop()

        # Publish to real Kafka broker if connected
        if self.is_connected and self.producer:
            try:
                future = self.producer.send(topic, key=key, value=formatted_payload)
                # Async callback or non-blocking flush
                print(f"[⚡ Kafka Event Published] Topic: {topic} | Type: {event_type} | ID: {event_id}")
            except Exception as e:
                print(f"[Kafka Publish Error] Failed to publish to {topic}: {e}")

        return formatted_payload

    def get_status(self) -> dict:
        """Returns status metrics and cluster health info."""
        return {
            'enabled': self.enabled,
            'kafka_library_installed': KAFKA_AVAILABLE,
            'is_connected': self.is_connected,
            'bootstrap_servers': self.bootstrap_servers,
            'security_protocol': self.security_protocol,
            'mode': self.metrics['mode'],
            'total_events_published': self.metrics['total_events_published'],
            'emergency_alerts_triggered': self.metrics['emergency_alerts_triggered'],
            'topics': [
                {
                    'name': name,
                    'topic_name': topic,
                    'message_count': self.metrics['topic_counts'].get(topic, 0)
                }
                for name, topic in self.TOPICS.items()
            ]
        }

    def get_recent_events(self, topic: str = None, limit: int = 50) -> list:
        """Returns recent events from the in-memory streaming log buffer."""
        if topic:
            filtered = [e for e in self.in_memory_events if e['topic'] == topic]
            return filtered[:limit]
        return self.in_memory_events[:limit]

    def _start_consumer_thread(self):
        """Launches a background daemon thread to process stream events."""
        t = threading.Thread(target=self._run_consumer_loop, daemon=True)
        t.start()

    def _run_consumer_loop(self):
        """Simulates background stream consumer listening for emergency triage events."""
        while True:
            time.sleep(15)
            # Periodic heartbeat check or consumer logic


# Global Singleton Instance
kafka_service = KAIreKafkaService()
