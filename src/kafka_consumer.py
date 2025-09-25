from kafka import KafkaConsumer
import os, json
from src.api.db import get_engine, Base, InferenceResult, sessionmaker


KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "model_results")


consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[KAFKA_BOOTSTRAP],
    auto_offset_reset='earliest',
    group_id="model_consumer_group",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)


engine = get_engine()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


for msg in consumer:
    data = msg.value
    session = Session()
    try:
        record = InferenceResult(
            input_data=json.dumps(data["input"]),
            prediction=float(data["prediction"])
        )
        session.add(record)
        session.commit()
        print(f"Saved to DB: {record.id}, prediction: {record.prediction}")
    except Exception as e:
        session.rollback()
        print("Error saving record:", e)
    finally:
        session.close()
