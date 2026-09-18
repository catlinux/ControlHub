from __future__ import annotations

from datetime import UTC, datetime

from argon2 import PasswordHasher
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from sqlmodel import select

from app.auth.service import audit, get_session
from app.db import db_session
from app.models import AuditLog, User

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])
_hasher = PasswordHasher()


def require_admin(request: Request):
    session = get_session(request)
    if session is None or session["role"] != "admin":
        raise HTTPException(status_code=403, detail="Acceso de administrador requerido.")
    csrf = request.headers.get("X-CSRF-Token")
    if not csrf or csrf != session["csrf_token"]:
        raise HTTPException(status_code=403, detail="CSRF inválido.")
    return session


class UserInput(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=12, max_length=256)
    role: str = Field(default="admin", pattern="^(admin|user)$")


class PasswordInput(BaseModel):
    password: str = Field(min_length=12, max_length=256)


class RoleInput(BaseModel):
    role: str = Field(pattern="^(admin|user)$")


@router.get("/users")
def list_users(request: Request):
    require_admin(request)
    with db_session() as db:
        return [
            {
                "id": user.id,
                "username": user.username,
                "role": user.role,
                "created_at": user.created_at,
            }
            for user in db.exec(select(User).order_by(User.username)).all()
        ]


@router.post("/users")
def create_user(payload: UserInput, request: Request):
    session = require_admin(request)
    username = payload.username.strip()
    with db_session() as db:
        if db.exec(select(User).where(User.username == username)).first() is not None:
            raise HTTPException(status_code=409, detail="El usuario ya existe.")
        user = User(
            username=username,
            password_hash=_hasher.hash(payload.password),
            role=payload.role,
            created_at=datetime.now(UTC).isoformat(),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        audit(session["user_id"], "user.created")
        return {"id": user.id, "username": user.username, "role": user.role}


@router.patch("/users/{user_id}/role")
def update_user_role(user_id: int, payload: RoleInput, request: Request):
    session = require_admin(request)
    with db_session() as db:
        user = db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        if user.id == session["user_id"] and payload.role != "admin":
            raise HTTPException(status_code=409, detail="No puedes quitarte tu propio rol de administrador.")
        user.role = payload.role
        db.add(user)
        db.commit()
        audit(session["user_id"], "user.role.changed")
        return {"id": user.id, "username": user.username, "role": user.role}


@router.patch("/users/{user_id}/password")
def update_user_password(user_id: int, payload: PasswordInput, request: Request):
    session = require_admin(request)
    with db_session() as db:
        user = db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        user.password_hash = _hasher.hash(payload.password)
        db.add(user)
        db.commit()
        audit(session["user_id"], "user.password.changed")
        return {"status": "ok"}


@router.delete("/users/{user_id}")
def delete_user(user_id: int, request: Request):
    session = require_admin(request)
    if user_id == session["user_id"]:
        raise HTTPException(status_code=409, detail="No puedes eliminar tu propia cuenta.")
    with db_session() as db:
        user = db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        db.delete(user)
        db.commit()
        audit(session["user_id"], "user.deleted")
        return {"status": "ok"}


@router.get("/audit")
def list_audit(request: Request, limit: int = 100):
    require_admin(request)
    limit = max(1, min(limit, 500))
    with db_session() as db:
        rows = db.exec(
            select(AuditLog).order_by(AuditLog.id.desc()).limit(limit)
        ).all()
        return [
            {
                "id": row.id,
                "user_id": row.user_id,
                "action": row.action,
                "created_at": row.created_at,
            }
            for row in rows
        ]
