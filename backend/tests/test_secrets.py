def test_secrets_require_admin(client) -> None:
    response = client.get("/api/v1/secrets")
    assert response.status_code == 403


def test_secret_crud_does_not_expose_value(client, monkeypatch) -> None:
    import app.api.secrets as secrets_api

    session = {
        "user_id": 1,
        "csrf_token": "test-csrf",
        "role": "admin",
        "username": "test-admin",
    }
    monkeypatch.setattr(secrets_api, "require_admin", lambda request: session)
    response = client.post(
        "/api/v1/secrets",
        headers={"X-CSRF-Token": "test-csrf"},
        json={"name": "test-secret", "description": "test", "value": "super-secret-value"},
    )
    assert response.status_code == 200
    assert "encrypted_value" not in response.json()

    secret_id = response.json()["id"]
    listed = client.get("/api/v1/secrets")
    assert listed.status_code == 200
    assert listed.json()[0]["name"] == "test-secret"
    assert "super-secret-value" not in listed.text
    assert "encrypted_value" not in listed.text

    deleted = client.delete(
        f"/api/v1/secrets/{secret_id}",
        headers={"X-CSRF-Token": "test-csrf"},
    )
    assert deleted.status_code == 200
