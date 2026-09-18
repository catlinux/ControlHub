import subprocess

from fastapi import APIRouter, HTTPException, Request

from app.auth.service import audit, get_session

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


def require_admin(request: Request):
    session = get_session(request)
    if session is None or session["role"] != "admin":
        raise HTTPException(status_code=403, detail="Acceso de administrador requerido.")

    csrf = request.headers.get("X-CSRF-Token")
    if not csrf or csrf != session["csrf_token"]:
        raise HTTPException(status_code=403, detail="CSRF inválido.")
    return session


@router.post("/restart")
def restart(request: Request):
    session = require_admin(request)
    audit(session["user_id"], "controlhub.restart.requested")
    subprocess.Popen(
        ["/usr/bin/sudo", "-n", "/bin/systemctl", "restart", "controlhub.service"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        env={"PATH": "/usr/bin:/bin"},
    )
    return {"status": "accepted"}
