from unittest.mock import patch


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "ML API is running 🚀", "status": "ok"}


@patch("src.kafka_producer.KafkaProducer")
def test_predict(mock_producer, client):
    data = {"trip_distance": 3.5, "passenger_count": 1}
    mock_instance = mock_producer.return_value
    mock_instance.send.return_value = None

    response = client.post("/predict", json=data)
    assert response.status_code == 200
    assert "prediction" in response.json()

