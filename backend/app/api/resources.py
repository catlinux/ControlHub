from __future__ import annotations

import json
from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from sqlmodel import select

from app.auth.service import audit, get_session
from app.db import db_session
from app.models import Category, Resource, ResourceTag, Tag

router = APIRouter(prefix="/api/v1", tags=["resources"])


class ResourceInput(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str = ""
    category_id: int | None = None
    resource_type: str = "web"
    url: str = ""
    host: str = ""
    port: int | None = Field(default=None, ge=1, le=65535)
    username: str = ""
    icon: str = ""
    status: str = "unknown"
    favorite: bool = False
    notes: str = ""
    metadata: dict = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)


def require_user(request: Request):
    session = get_session(request)
    if session is None:
        raise HTTPException(status_code=401, detail="Autenticación requerida.")
    return session


def require_csrf(request: Request, session) -> None:
    token = request.headers.get("X-CSRF-Token")
    if not token or token != session["csrf_token"]:
        raise HTTPException(status_code=403, detail="CSRF inválido.")


def serialize_resource(db, resource: Resource) -> dict:
    tag_rows = db.exec(
        select(Tag)
        .join(ResourceTag, ResourceTag.tag_id == Tag.id)
        .where(ResourceTag.resource_id == resource.id)
    ).all()
    return {
        "id": resource.id,
        "name": resource.name,
        "description": resource.description,
        "category_id": resource.category_id,
        "resource_type": resource.resource_type,
        "url": resource.url,
        "host": resource.host,
        "port": resource.port,
        "username": resource.username,
        "icon": resource.icon,
        "status": resource.status,
        "favorite": resource.favorite,
        "notes": resource.notes,
        "metadata": json.loads(resource.metadata_json or "{}"),
        "tags": [tag.name for tag in tag_rows],
        "created_at": resource.created_at,
        "updated_at": resource.updated_at,
    }


def sync_tags(db, resource_id: int, names: list[str]) -> None:
    normalized = sorted({name.strip() for name in names if name.strip()})
    existing = db.exec(
        select(ResourceTag).where(ResourceTag.resource_id == resource_id)
    ).all()
    for link in existing:
        db.delete(link)

    for name in normalized:
        tag = db.exec(select(Tag).where(Tag.name == name)).first()
        if tag is None:
            tag = Tag(name=name, created_at=datetime.now(UTC).isoformat())
            db.add(tag)
            db.commit()
            db.refresh(tag)
        db.add(ResourceTag(resource_id=resource_id, tag_id=tag.id))


@router.get("/resources")
def list_resources(
    request: Request,
    search: str = "",
    category_id: int | None = None,
    tag: str = "",
    favorite: bool | None = None,
):
    require_user(request)
    with db_session() as db:
        statement = select(Resource).order_by(Resource.favorite.desc(), Resource.name)
        if search.strip():
            pattern = "%" + search.strip() + "%"
            statement = statement.where(
                (Resource.name.ilike(pattern))
                | (Resource.description.ilike(pattern))
                | (Resource.host.ilike(pattern))
                | (Resource.url.ilike(pattern))
            )
        if category_id is not None:
            statement = statement.where(Resource.category_id == category_id)
        if favorite is not None:
            statement = statement.where(Resource.favorite == favorite)
        resources = db.exec(statement).all()

        if tag.strip():
            filtered = []
            for resource in resources:
                names = db.exec(
                    select(Tag)
                    .join(ResourceTag, ResourceTag.tag_id == Tag.id)
                    .where(ResourceTag.resource_id == resource.id)
                ).all()
                if tag.strip() in {item.name for item in names}:
                    filtered.append(resource)
            resources = filtered

        return [serialize_resource(db, resource) for resource in resources]


@router.get("/resources/{resource_id}")
def get_resource(resource_id: int, request: Request):
    require_user(request)
    with db_session() as db:
        resource = db.get(Resource, resource_id)
        if resource is None:
            raise HTTPException(status_code=404, detail="Recurso no encontrado.")
        return serialize_resource(db, resource)


@router.post("/resources")
def create_resource(payload: ResourceInput, request: Request):
    session = require_user(request)
    require_csrf(request, session)
    now = datetime.now(UTC).isoformat()
    with db_session() as db:
        resource = Resource(
            name=payload.name.strip(),
            description=payload.description.strip(),
            category_id=payload.category_id,
            resource_type=payload.resource_type.strip() or "web",
            url=payload.url.strip(),
            host=payload.host.strip(),
            port=payload.port,
            username=payload.username.strip(),
            icon=payload.icon.strip(),
            status=payload.status.strip() or "unknown",
            favorite=payload.favorite,
            notes=payload.notes.strip(),
            metadata_json=json.dumps(payload.metadata, ensure_ascii=False),
            created_at=now,
            updated_at=now,
        )
        db.add(resource)
        db.commit()
        db.refresh(resource)
        sync_tags(db, resource.id, payload.tags)
        db.commit()
        audit(session["user_id"], "resource.created")
        return serialize_resource(db, resource)


@router.put("/resources/{resource_id}")
def update_resource(resource_id: int, payload: ResourceInput, request: Request):
    session = require_user(request)
    require_csrf(request, session)
    with db_session() as db:
        resource = db.get(Resource, resource_id)
        if resource is None:
            raise HTTPException(status_code=404, detail="Recurso no encontrado.")

        resource.name = payload.name.strip()
        resource.description = payload.description.strip()
        resource.category_id = payload.category_id
        resource.resource_type = payload.resource_type.strip() or "web"
        resource.url = payload.url.strip()
        resource.host = payload.host.strip()
        resource.port = payload.port
        resource.username = payload.username.strip()
        resource.icon = payload.icon.strip()
        resource.status = payload.status.strip() or "unknown"
        resource.favorite = payload.favorite
        resource.notes = payload.notes.strip()
        resource.metadata_json = json.dumps(payload.metadata, ensure_ascii=False)
        resource.updated_at = datetime.now(UTC).isoformat()

        db.add(resource)
        db.commit()
        sync_tags(db, resource.id, payload.tags)
        db.commit()
        audit(session["user_id"], "resource.updated")
        return serialize_resource(db, resource)


@router.delete("/resources/{resource_id}")
def delete_resource(resource_id: int, request: Request):
    session = require_user(request)
    require_csrf(request, session)
    with db_session() as db:
        resource = db.get(Resource, resource_id)
        if resource is None:
            raise HTTPException(status_code=404, detail="Recurso no encontrado.")

        for link in db.exec(
            select(ResourceTag).where(ResourceTag.resource_id == resource_id)
        ).all():
            db.delete(link)
        db.delete(resource)
        db.commit()
        audit(session["user_id"], "resource.deleted")
        return {"status": "ok"}


@router.get("/categories")
def list_categories(request: Request):
    require_user(request)
    with db_session() as db:
        return db.exec(select(Category).order_by(Category.name)).all()


@router.post("/categories")
def create_category(name: str, request: Request):
    session = require_user(request)
    require_csrf(request, session)
    normalized = name.strip()
    if not normalized:
        raise HTTPException(status_code=400, detail="El nombre es obligatorio.")

    with db_session() as db:
        existing = db.exec(select(Category).where(Category.name == normalized)).first()
        if existing:
            return existing

        category = Category(
            name=normalized,
            created_at=datetime.now(UTC).isoformat(),
        )
        db.add(category)
        db.commit()
        db.refresh(category)
        audit(session["user_id"], "category.created")
        return category


@router.get("/tags")
def list_tags(request: Request):
    require_user(request)
    with db_session() as db:
        return db.exec(select(Tag).order_by(Tag.name)).all()
