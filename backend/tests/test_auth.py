from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_unauthenticated_me():
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 200
    assert response.json()["authenticated"] is False

def test_restart_requires_auth():
    response = client.post("/api/v1/admin/restart")
    assert response.status_code == 403
