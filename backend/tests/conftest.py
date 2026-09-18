import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("CONTROLHUB_ADMIN_USERNAME", "test-admin")
    monkeypatch.setenv("CONTROLHUB_ADMIN_PASSWORD", "test-password")
    with TestClient(app) as test_client:
        yield test_client
