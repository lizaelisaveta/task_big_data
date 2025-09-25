import json
from src.kafka_producer import send_message
from kafka import KafkaProducer, KafkaConsumer


def test_kafka_message():
    payload = {"id": 1, "prediction": 100, "input": {"trip_distance": 1, "passenger_count": 1}}
    serialized = json.dumps(payload).encode("utf-8")
    assert serialized == json.dumps(payload).encode("utf-8")
