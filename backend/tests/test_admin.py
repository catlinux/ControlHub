def test_admin_users_and_audit(client, monkeypatch) -> None:
    import app.api.admin_management as admin_api

    session = {
        "user_id": 1,
        "csrf_token": "test-csrf",
        "role": "admin",
        "username": "test-admin",
    }
    monkeypatch.setattr(admin_api, "require_admin", lambda request: session)

    response = client.post(
        "/api/v1/admin/users",
        headers={"X-CSRF-Token": "test-csrf"},
        json={"username": "managed-user", "password": "strong-test-password", "role": "user"},
    )
    assert response.status_code == 200
    user_id = response.json()["id"]

    users = client.get("/api/v1/admin/users")
    assert users.status_code == 200
    assert any(user["username"] == "managed-user" for user in users.json())

    role = client.patch(
        f"/api/v1/admin/users/{user_id}/role",
        headers={"X-CSRF-Token": "test-csrf"},
        json={"role": "admin"},
    )
    assert role.status_code == 200

    password = client.patch(
        f"/api/v1/admin/users/{user_id}/password",
        headers={"X-CSRF-Token": "test-csrf"},
        json={"password": "another-strong-password"},
    )
    assert password.status_code == 200

    audit = client.get("/api/v1/admin/audit")
    assert audit.status_code == 200
    assert any(row["action"] == "user.created" for row in audit.json())

    deleted = client.delete(
        f"/api/v1/admin/users/{user_id}",
        headers={"X-CSRF-Token": "test-csrf"},
    )
    assert deleted.status_code == 200


def test_admin_read_endpoints_do_not_require_csrf(client, monkeypatch) -> None:
    import app.api.admin_management as admin_api
    import app.api.secrets as secrets_api

    session = {
        "user_id": 1,
        "csrf_token": "test-csrf",
        "role": "admin",
        "username": "test-admin",
    }
    monkeypatch.setattr(admin_api, "get_session", lambda request: session)
    monkeypatch.setattr(secrets_api, "get_session", lambda request: session)

    assert client.get("/api/v1/admin/users").status_code == 200
    assert client.get("/api/v1/admin/audit").status_code == 200
    assert client.get("/api/v1/secrets").status_code == 200
