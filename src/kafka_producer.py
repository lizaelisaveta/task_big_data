from kafka import KafkaProducer
import os, json


KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")


producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def send_message(topic, payload):
    producer.send(topic, payload)
    producer.flush()
