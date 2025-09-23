from kafka import KafkaConsumer
import os, json


KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "model_results")


consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[KAFKA_BOOTSTRAP],
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)


for msg in consumer:
    print("Received:", msg.value)
    
