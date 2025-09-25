import pandas as pd
import joblib
import tempfile
from src.train import train
from sklearn.ensemble import RandomForestRegressor


def test_train_saves_model():
    df = pd.DataFrame({
        "trip_distance": [1, 2, 3, 4],
        "passenger_count": [1, 2, 1, 2],
        "duration_sec": [600, 1200, 1800, 2400]
    })

    with tempfile.NamedTemporaryFile(suffix=".parquet") as data_file, \
         tempfile.NamedTemporaryFile(suffix=".joblib") as model_file:
        df.to_parquet(data_file.name)
        train(data_file.name, model_file.name, n_estimators=10, test_size=0.5, random_state=42)

        model = joblib.load(model_file.name)
        assert isinstance(model, RandomForestRegressor)
        preds = model.predict(df[["trip_distance", "passenger_count"]])
        assert len(preds) == len(df)
