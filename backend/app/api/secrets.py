from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from sqlmodel import select

from app.auth.service import audit, get_session
from app.db import db_session
from app.models import Secret
from app.secrets import SecretStoreError, encrypt

router = APIRouter(prefix="/api/v1/secrets", tags=["secrets"])


def require_admin(request: Request, *, check_csrf: bool = True):
    session = get_session(request)
    if session is None or session["role"] != "admin":
        raise HTTPException(status_code=403, detail="Acceso de administrador requerido.")
    if check_csrf:
        csrf = request.headers.get("X-CSRF-Token")
        if not csrf or csrf != session["csrf_token"]:
            raise HTTPException(status_code=403, detail="CSRF inválido.")
    return session


class SecretInput(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=500)
    value: str = Field(min_length=1)


def serialize(secret: Secret) -> dict:
    return {
        "id": secret.id,
        "name": secret.name,
        "description": secret.description,
        "created_at": secret.created_at,
        "updated_at": secret.updated_at,
    }


@router.get("")
def list_secrets(request: Request):
    require_admin(request, check_csrf=False)
    with db_session() as db:
        return [serialize(item) for item in db.exec(select(Secret).order_by(Secret.name)).all()]


@router.post("")
def create_secret(payload: SecretInput, request: Request):
    session = require_admin(request)
    try:
        encrypted = encrypt(payload.value)
    except SecretStoreError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    now = datetime.now(UTC).isoformat()
    with db_session() as db:
        existing = db.exec(select(Secret).where(Secret.name == payload.name.strip())).first()
        if existing is not None:
            raise HTTPException(status_code=409, detail="Ya existe un secreto con ese nombre.")
        secret = Secret(
            name=payload.name.strip(),
            description=payload.description.strip(),
            encrypted_value=encrypted,
            created_at=now,
            updated_at=now,
        )
        db.add(secret)
        db.commit()
        db.refresh(secret)
        audit(session["user_id"], "secret.created")
        return serialize(secret)


@router.put("/{secret_id}")
def update_secret(secret_id: int, payload: SecretInput, request: Request):
    session = require_admin(request)
    try:
        encrypted = encrypt(payload.value)
    except SecretStoreError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    with db_session() as db:
        secret = db.get(Secret, secret_id)
        if secret is None:
            raise HTTPException(status_code=404, detail="Secreto no encontrado.")
        duplicate = db.exec(
            select(Secret).where(Secret.name == payload.name.strip(), Secret.id != secret_id)
        ).first()
        if duplicate is not None:
            raise HTTPException(status_code=409, detail="Ya existe un secreto con ese nombre.")
        secret.name = payload.name.strip()
        secret.description = payload.description.strip()
        secret.encrypted_value = encrypted
        secret.updated_at = datetime.now(UTC).isoformat()
        db.add(secret)
        db.commit()
        db.refresh(secret)
        audit(session["user_id"], "secret.updated")
        return serialize(secret)


@router.delete("/{secret_id}")
def delete_secret(secret_id: int, request: Request):
    session = require_admin(request)
    with db_session() as db:
        secret = db.get(Secret, secret_id)
        if secret is None:
            raise HTTPException(status_code=404, detail="Secreto no encontrado.")
        db.delete(secret)
        db.commit()
        audit(session["user_id"], "secret.deleted")
        return {"status": "ok"}
