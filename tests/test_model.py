from src.model import ModelWrapper


def test_model_prediction():
    model = ModelWrapper("model/rf_2016-03.joblib")
    sample_input = {"trip_distance": 2.5, "passenger_count": 1}
    pred = model.predict(sample_input)
    assert isinstance(pred, float)
    assert pred > 0
