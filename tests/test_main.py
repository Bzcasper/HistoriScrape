from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI-Integrated API is running."}

def test_train_model():
    response = client.post("/train-model", json={"data": "sample"})
    assert response.status_code == 200
    assert response.json() == {"message": "Model training initiated."}
