
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_greeting():
    response = client.post("/chat", json={"message": "hello"})
    assert response.status_code == 200
    assert "Hello" in response.json()["reply"]


def test_balance_enquiry():
    response = client.post("/chat", json={"message": "What is my balance?"})
    assert response.status_code == 200
    assert "not connected to a real bank account" in response.json()["reply"]


def test_transfer_request():
    response = client.post("/chat", json={"message": "I want to transfer 500 rupees"})
    assert response.status_code == 200
    assert "cannot transfer money" in response.json()["reply"]
