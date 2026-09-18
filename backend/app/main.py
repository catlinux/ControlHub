import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import app.models
from app.api.admin import router as admin_router
from app.api.auth import router as auth_router
from app.api.resources import router as resources_router
from app.auth.service import ensure_admin
from app.db import init_db

FRONTEND_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    ensure_admin(
        os.getenv("CONTROLHUB_ADMIN_USERNAME", ""),
        os.getenv("CONTROLHUB_ADMIN_PASSWORD", ""),
    )
    yield


app = FastAPI(title="ControlHub API", version="0.2.0", lifespan=lifespan)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(resources_router)


@app.get("/api/v1/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


if FRONTEND_DIST.exists():
    app.mount(
        "/assets",
        StaticFiles(directory=FRONTEND_DIST / "assets"),
        name="assets",
    )

    @app.get("/{path:path}", include_in_schema=False)
    def frontend(path: str):
        requested = FRONTEND_DIST / path
        if path and requested.is_file():
            return FileResponse(requested)
        return FileResponse(FRONTEND_DIST / "index.html")
