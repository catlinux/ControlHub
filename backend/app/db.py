from __future__ import annotations

import os
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine


def database_url() -> str:
    return os.getenv("DATABASE_URL", "sqlite:///data/controlhub.db").strip()


def resolved_database_url() -> str:
    value = database_url()
    if value.startswith("sqlite:///") and not value.startswith("sqlite:////"):
        path = Path(value.removeprefix("sqlite:///"))
        if not path.is_absolute():
            path = Path(__file__).resolve().parents[2] / path
        return "sqlite:///" + str(path)
    return value


engine = create_engine(
    resolved_database_url(),
    connect_args={"check_same_thread": False}
    if resolved_database_url().startswith("sqlite:")
    else {},
)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def db_session() -> Session:
    return Session(engine)
