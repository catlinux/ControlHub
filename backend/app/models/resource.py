from __future__ import annotations

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str
    role: str = "admin"
    created_at: str


class AuthSession(SQLModel, table=True):
    __tablename__ = "sessions"

    id: str = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    csrf_token: str
    expires_at: str
    created_at: str


class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_log"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id")
    action: str = Field(index=True)
    created_at: str


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str = ""
    created_at: str


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    created_at: str


class ResourceTag(SQLModel, table=True):
    __tablename__ = "resource_tags"

    resource_id: int = Field(foreign_key="resources.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)


class Secret(SQLModel, table=True):
    __tablename__ = "secrets"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str = ""
    encrypted_value: str
    created_at: str
    updated_at: str


class Resource(SQLModel, table=True):
    __tablename__ = "resources"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str = ""
    category_id: int | None = Field(default=None, foreign_key="categories.id", index=True)
    resource_type: str = Field(default="web", index=True)
    url: str = ""
    host: str = ""
    port: int | None = None
    username: str = ""
    icon: str = ""
    status: str = "unknown"
    favorite: bool = False
    notes: str = ""
    metadata_json: str = "{}"
    created_at: str
    updated_at: str
