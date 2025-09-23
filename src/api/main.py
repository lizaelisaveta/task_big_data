from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, json
from src.model import ModelWrapper
from src.api.db import get_session, InferenceResult
from src.kafka_producer import send_message


MODEL_PATH = os.getenv("MODEL_PATH", "model/rf_2016-03.joblib")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "model_results")


app = FastAPI()
model = ModelWrapper(MODEL_PATH)


class InputSchema(BaseModel):
    trip_distance: float = None
    passenger_count: int = None


@app.post("/predict")
def predict(payload: InputSchema):
    inp = payload.dict()
    try:
        pred = model.predict(inp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    session = get_session()
    record = InferenceResult(input_data=json.dumps(inp), prediction=float(pred))
    session.add(record)
    session.commit()
    session.refresh(record)
    session.close()

    send_message(KAFKA_TOPIC, {"id": record.id, "prediction": pred, "input": inp})

    return {"id": record.id, "prediction": pred}
