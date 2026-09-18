import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("CONTROLHUB_ADMIN_USERNAME", "test-admin")
    monkeypatch.setenv("CONTROLHUB_ADMIN_PASSWORD", "test-password")
    monkeypatch.setenv("CONTROLHUB_SECRET_KEY", "kjyRTXTmx0H69SJBlfDnYmlaIzx10jdIPqty6i_e2ZE=")
    with TestClient(app, base_url="https://testserver") as test_client:
        yield test_client
