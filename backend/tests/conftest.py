from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine


@pytest.fixture()
def client(monkeypatch, tmp_path) -> TestClient:
    db_path = Path(tmp_path) / "controlhub-test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("CONTROLHUB_ADMIN_USERNAME", "test-admin")
    monkeypatch.setenv("CONTROLHUB_ADMIN_PASSWORD", "test-password")
    monkeypatch.setenv("CONTROLHUB_SECRET_KEY", "kjyRTXTmx0H69SJBlfDnYmlaIzx10jdIPqty6i_e2ZE=")

    from app import db
    from app.main import app

    test_engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )
    monkeypatch.setattr(db, "engine", test_engine)

    try:
        with TestClient(app, base_url="https://testserver") as test_client:
            yield test_client
    finally:
        test_engine.dispose()
