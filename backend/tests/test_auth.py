def test_unauthenticated_me(client) -> None:
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 200
    assert response.json()["authenticated"] is False


def test_restart_requires_auth(client) -> None:
    response = client.post("/api/v1/admin/restart")
    assert response.status_code == 403


def test_login_rejects_invalid_credentials(client) -> None:
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "nonexistent", "password": "invalid"},
    )
    assert response.status_code == 200
    assert response.json()["authenticated"] is False
