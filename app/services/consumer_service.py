import json
import os
import sys
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'math-operations-logs',
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
)


def consume_logs():
    try:
        for message in consumer:
            log = message.value
            print(f"Log: {log['event']} with payload: {log['payload']}")
    except KeyboardInterrupt:
        print("Stopping consumer...")
        consumer.close()
        sys.exit(0)


if __name__ == "__main__":
    print("Starting Kafka log consumer...")
    consume_logs()
