from kafka import KafkaProducer
import os, json


KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")

def get_producer():
    return KafkaProducer(
        bootstrap_servers=[KAFKA_BOOTSTRAP],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


def send_message(topic, payload):
    producer = get_producer()
    producer.send(topic, payload)
    producer.flush()
