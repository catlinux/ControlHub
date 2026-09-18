from __future__ import annotations

import os
import secrets
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from fastapi import Request

_hasher = PasswordHasher()
_TTL = timedelta(hours=12)


def utcnow() -> datetime:
    return datetime.now(UTC)


def _db_path() -> Path:
    value = os.getenv("DATABASE_URL", "").strip()
    if value.startswith("sqlite:///"):
        value = value.removeprefix("sqlite:///")
    return Path(value or "data/controlhub.db")


def _connect() -> sqlite3.Connection:
    path = _db_path()
    if not path.is_absolute():
        path = Path(__file__).resolve().parents[3] / path
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    return db


def init_auth_db() -> None:
    with _connect() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'admin',
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                csrf_token TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )


def ensure_admin(username: str, password: str) -> None:
    if not username or not password:
        return
    with _connect() as db:
        row = db.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()
        if row is None:
            db.execute(
                "INSERT INTO users(username, password_hash, role, created_at) "
                "VALUES (?, ?, 'admin', ?)",
                (username, _hasher.hash(password), utcnow().isoformat()),
            )


def authenticate(username: str, password: str) -> Any:
    with _connect() as db:
        row = db.execute(
            "SELECT id, username, password_hash, role "
            "FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    if row is None:
        return None
    try:
        return row if _hasher.verify(row["password_hash"], password) else None
    except VerificationError:
        return None


def create_session(user_id: int) -> tuple[str, str]:
    session_id = secrets.token_urlsafe(32)
    csrf_token = secrets.token_urlsafe(32)
    expires = utcnow() + _TTL
    with _connect() as db:
        db.execute(
            "INSERT INTO sessions VALUES (?, ?, ?, ?, ?)",
            (
                session_id,
                user_id,
                csrf_token,
                expires.isoformat(),
                utcnow().isoformat(),
            ),
        )
    return session_id, csrf_token


def get_session(request: Request) -> Any:
    session_id = request.cookies.get("controlhub_session")
    if not session_id:
        return None
    with _connect() as db:
        row = db.execute(
            """
            SELECT s.id, s.user_id, s.csrf_token, s.expires_at, u.username, u.role
            FROM sessions s
            JOIN users u ON u.id = s.user_id
            WHERE s.id = ?
            """,
            (session_id,),
        ).fetchone()
    if row is None:
        return None
    try:
        if datetime.fromisoformat(row["expires_at"]) <= utcnow():
            delete_session(session_id)
            return None
    except ValueError:
        delete_session(session_id)
        return None
    return row


def delete_session(session_id: str) -> None:
    with _connect() as db:
        db.execute("DELETE FROM sessions WHERE id = ?", (session_id,))


def audit(user_id: int, action: str) -> None:
    with _connect() as db:
        db.execute(
            "INSERT INTO audit_log(user_id, action, created_at) VALUES (?, ?, ?)",
            (user_id, action, utcnow().isoformat()),
        )
