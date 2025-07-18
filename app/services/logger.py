from kafka import KafkaProducer
import json
import os


producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def log_event(event_type: str, payload: dict):
    message = {
        "event": event_type,
        "payload": payload
    }
    producer.send("math-operations-logs", value=message)
