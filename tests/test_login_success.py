from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_with_valid_credentials_succeeds():
    # В app.db уже есть пользователь admin/admin
    payload = {"username": "admin", "password": "admin"}
    resp = client.post("/login", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["user"] == "admin"
    assert "token" in body
