import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("CONTROLHUB_ADMIN_USERNAME", "test-admin")
    monkeypatch.setenv("CONTROLHUB_ADMIN_PASSWORD", "test-password")
    monkeypatch.setenv("CONTROLHUB_SECRET_KEY", "8Q7j8Y4Y7Q9K2c6qk0u3WQ5Jm5Xf5l1u1w2m3n4o5p6=")
    with TestClient(app, base_url="https://testserver") as test_client:
        yield test_client
