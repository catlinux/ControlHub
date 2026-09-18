from pathlib import Path
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.admin import router as admin_router
from app.api.auth import router as auth_router
from app.auth.service import ensure_admin, init_auth_db

app = FastAPI(title="ControlHub API", version="0.1.0")
app.include_router(auth_router)
app.include_router(admin_router)

FRONTEND_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"

@app.on_event("startup")
def startup() -> None:
    init_auth_db()
    ensure_admin(os.getenv("CONTROLHUB_ADMIN_USERNAME", ""), os.getenv("CONTROLHUB_ADMIN_PASSWORD", ""))

@app.get("/api/v1/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}

if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{path:path}", include_in_schema=False)
    def frontend(path: str):
        requested = FRONTEND_DIST / path
        if path and requested.is_file():
            return FileResponse(requested)
        return FileResponse(FRONTEND_DIST / "index.html")
