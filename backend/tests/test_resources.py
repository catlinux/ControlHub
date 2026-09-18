from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_resources_requires_auth():
    response = client.get("/api/v1/resources")
    assert response.status_code == 401


def test_favorite_requires_auth():
    response = client.patch(
        "/api/v1/resources/1/favorite",
        json={"favorite": True},
    )
    assert response.status_code == 401
