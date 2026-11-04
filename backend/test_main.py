from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def reset_demo_state():
    import main
    main.pending_transfer = None
    main.mock_transactions.clear()


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
    reset_demo_state()
    response = client.post(
        "/chat",
        json={"message": "I want to transfer 500 rupees"}
    )
    assert response.status_code == 200
    assert "cannot transfer money" in response.json()["reply"]


def test_transfer_confirmation_and_correct_code():
    reset_demo_state()

    response = client.post(
        "/chat",
        json={"message": "Send 500 rupees to Rahul"}
    )
    assert "confirm" in response.json()["reply"].lower()

    response = client.post("/chat", json={"message": "YES"})
    assert "2468" in response.json()["reply"]

    response = client.post("/chat", json={"message": "2468"})
    assert "verification successful" in response.json()["reply"].lower()
    assert response.json()["receipt"]["recipient"] == "rahul"
    assert response.json()["receipt"]["amount"] == 500


def test_incorrect_verification_code():
    reset_demo_state()

    client.post(
        "/chat",
        json={"message": "Send 700 rupees to Priya"}
    )
    client.post("/chat", json={"message": "YES"})

    response = client.post("/chat", json={"message": "1234"})

    assert "incorrect" in response.json()["reply"].lower()
    assert "receipt" not in response.json()


def test_cancel_transfer():
    reset_demo_state()

    client.post(
        "/chat",
        json={"message": "Send 1000 rupees to Priya"}
    )

    response = client.post("/chat", json={"message": "NO"})

    assert "cancelled" in response.json()["reply"].lower()


def test_cancel_during_verification():
    reset_demo_state()

    client.post(
        "/chat",
        json={"message": "Send 700 rupees to Priya"}
    )
    client.post("/chat", json={"message": "YES"})

    response = client.post("/chat", json={"message": "NO"})

    assert "cancelled" in response.json()["reply"].lower()

    import main
    assert main.pending_transfer is None
