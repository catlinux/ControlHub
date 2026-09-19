from __future__ import annotations

import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect
from sqlmodel import Session


def database_url() -> str:
    return os.getenv("DATABASE_URL", "sqlite:///data/controlhub.db").strip()


def resolved_database_url() -> str:
    value = database_url()
    if value.startswith("sqlite:///") and not value.startswith("sqlite:////"):
        path = Path(value.removeprefix("sqlite:///"))
        if not path.is_absolute():
            path = Path(__file__).resolve().parents[2] / path
        path.parent.mkdir(parents=True, exist_ok=True)
        return "sqlite:///" + str(path)
    return value


engine = create_engine(
    resolved_database_url(),
    connect_args={"check_same_thread": False}
    if resolved_database_url().startswith("sqlite:")
    else {},
)


def _alembic_config() -> Config:
    config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", resolved_database_url())
    return config


def init_db() -> None:
    inspector = inspect(engine)
    if inspector.has_table("users") and not inspector.has_table("alembic_version"):
        command.stamp(_alembic_config(), "0001_initial")
    command.upgrade(_alembic_config(), "head")


def db_session() -> Session:
    return Session(engine)
