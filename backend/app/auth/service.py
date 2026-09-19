from __future__ import annotations

import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from fastapi import Request
from sqlmodel import select

from app.db import db_session
from app.models import AuditLog, AuthSession, User

_hasher = PasswordHasher()
_TTL = timedelta(hours=12)


def utcnow() -> datetime:
    return datetime.now(UTC)


def ensure_admin(username: str, password: str) -> None:
    if not username or not password:
        return
    with db_session() as db:
        user = db.exec(select(User).where(User.username == username)).first()
        if user is None:
            db.add(
                User(
                    username=username,
                    password_hash=_hasher.hash(password),
                    role="admin",
                    created_at=utcnow().isoformat(),
                )
            )
            db.commit()


def authenticate(username: str, password: str) -> Any:
    with db_session() as db:
        user = db.exec(select(User).where(User.username == username)).first()
        if user is None:
            return None
        try:
            if not _hasher.verify(user.password_hash, password):
                return None
        except VerificationError:
            return None
        return user


def create_session(user_id: int) -> tuple[str, str]:
    session_id = secrets.token_urlsafe(32)
    csrf_token = secrets.token_urlsafe(32)
    now = utcnow()
    expires = now + _TTL
    with db_session() as db:
        db.add(
            AuthSession(
                id=session_id,
                user_id=user_id,
                csrf_token=csrf_token,
                expires_at=expires.isoformat(),
                created_at=now.isoformat(),
            )
        )
        db.commit()
    return session_id, csrf_token


def get_session(request: Request) -> Any:
    session_id = request.cookies.get("controlhub_session")
    if not session_id:
        return None
    with db_session() as db:
        session = db.get(AuthSession, session_id)
        if session is None:
            return None
        try:
            if datetime.fromisoformat(session.expires_at) <= utcnow():
                db.delete(session)
                db.commit()
                return None
        except ValueError:
            db.delete(session)
            db.commit()
            return None
        user = db.get(User, session.user_id)
        if user is None:
            return None
        return {
            "id": session.id,
            "user_id": user.id,
            "csrf_token": session.csrf_token,
            "expires_at": session.expires_at,
            "username": user.username,
            "role": user.role,
        }


def delete_session(session_id: str) -> None:
    with db_session() as db:
        session = db.get(AuthSession, session_id)
        if session is not None:
            db.delete(session)
            db.commit()


def audit(user_id: int, action: str) -> None:
    with db_session() as db:
        db.add(
            AuditLog(
                user_id=user_id,
                action=action,
                created_at=utcnow().isoformat(),
            )
        )
        db.commit()
