import joblib
import numpy as np
import pandas as pd


class ModelWrapper:
    def __init__(self, model_path):
        self.model = joblib.load(model_path)

    def predict(self, input_dict):
        df = pd.DataFrame([input_dict])
        preds = self.model.predict(df)
        return float(preds[0])
