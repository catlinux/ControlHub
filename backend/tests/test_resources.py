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


def test_resource_crud_and_filters(monkeypatch) -> None:
    import app.api.resources as resources_api

    session = {"user_id": 1, "csrf_token": "test-csrf", "role": "admin", "username": "test"}
    monkeypatch.setattr(resources_api, "require_user", lambda request: session)
    monkeypatch.setattr(resources_api, "require_csrf", lambda request, session: None)
    monkeypatch.setattr(resources_api, "audit", lambda user_id, action: None)

    payload = {
        "name": "Test ControlHub Resource",
        "description": "Integration test",
        "resource_type": "ssh",
        "host": "192.0.2.10",
        "port": 2222,
        "username": "tester",
        "favorite": False,
        "tags": ["integration-test", "ssh"],
    }
    response = client.post("/api/v1/resources", json=payload)
    assert response.status_code == 200
    resource = response.json()
    resource_id = resource["id"]

    try:
        assert resource["name"] == payload["name"]
        assert resource["tags"] == ["integration-test", "ssh"]

        response = client.get("/api/v1/resources", params={"tag": "integration-test"})
        assert response.status_code == 200
        assert any(item["id"] == resource_id for item in response.json())

        response = client.patch(
            f"/api/v1/resources/{resource_id}/favorite",
            json={"favorite": True},
        )
        assert response.status_code == 200
        assert response.json()["favorite"] is True

        updated = {**payload, "name": "Updated ControlHub Resource", "favorite": True}
        response = client.put(f"/api/v1/resources/{resource_id}", json=updated)
        assert response.status_code == 200
        assert response.json()["name"] == "Updated ControlHub Resource"

        response = client.get(f"/api/v1/resources/{resource_id}")
        assert response.status_code == 200
        assert response.json()["favorite"] is True
    finally:
        response = client.delete(f"/api/v1/resources/{resource_id}")
        assert response.status_code == 200


def test_category_creation_requires_name(monkeypatch) -> None:
    import app.api.resources as resources_api

    session = {"user_id": 1, "csrf_token": "test-csrf", "role": "admin", "username": "test"}
    monkeypatch.setattr(resources_api, "require_user", lambda request: session)
    monkeypatch.setattr(resources_api, "require_csrf", lambda request, session: None)
    monkeypatch.setattr(resources_api, "audit", lambda user_id, action: None)

    response = client.post("/api/v1/categories", params={"name": "   "})
    assert response.status_code == 400
