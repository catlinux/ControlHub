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



def test_login_accepts_valid_credentials(client) -> None:
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test-admin", "password": "test-password"},
    )
    assert response.status_code == 200
    assert response.json() == {"authenticated": True, "username": "test-admin"}
    assert "controlhub_session" in response.cookies
    assert "controlhub_csrf" in response.cookies

    session_response = client.get("/api/v1/auth/me")
    assert session_response.status_code == 200
    assert session_response.json() == {
        "authenticated": True,
        "username": "test-admin",
        "role": "admin",
    }
