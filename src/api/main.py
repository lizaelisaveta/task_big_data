from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, json
from src.model import ModelWrapper
from src.api.db import init_db
from src.kafka_producer import send_message


MODEL_PATH = os.getenv("MODEL_PATH", "model/rf_2016-03.joblib")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "model_results")


app = FastAPI()
model = ModelWrapper(MODEL_PATH)


class InputSchema(BaseModel):
    trip_distance: float = None
    passenger_count: int = None


@app.get("/")
def root():
    return {"status": "ok", "message": "ML API is running 🚀"}


@app.post("/predict")
def predict(payload: InputSchema):
    inp = payload.dict()
    try:
        pred = model.predict(inp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    send_message(KAFKA_TOPIC, {"prediction": pred, "input": inp})

    return {"prediction": pred}


if __name__ == "__main__":
    init_db()
