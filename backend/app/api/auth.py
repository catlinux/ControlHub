from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import RedirectResponse

from app.auth.service import (
    audit,
    authenticate,
    create_session,
    delete_session,
    get_session,
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.get("/me")
def me(request: Request):
    session = get_session(request)
    if session is None:
        return {"authenticated": False}
    return {
        "authenticated": True,
        "username": session["username"],
        "role": session["role"],
    }


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    user = authenticate(username, password)
    if user is None:
        return {"authenticated": False, "error": "Credenciales no válidas."}

    session_id, csrf_token = create_session(user["id"])
    audit(user["id"], "auth.login")
    response = RedirectResponse("/", status_code=303)
    response.set_cookie(
        "controlhub_session",
        session_id,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=43200,
        path="/",
    )
    response.set_cookie(
        "controlhub_csrf",
        csrf_token,
        httponly=False,
        secure=True,
        samesite="lax",
        max_age=43200,
        path="/",
    )
    return response


@router.post("/logout")
def logout(request: Request):
    session = get_session(request)
    if session is None:
        raise HTTPException(status_code=401, detail="Sesión no válida.")

    csrf = request.headers.get("X-CSRF-Token")
    if not csrf or csrf != session["csrf_token"]:
        raise HTTPException(status_code=403, detail="CSRF inválido.")

    audit(session["user_id"], "auth.logout")
    delete_session(session["id"])
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("controlhub_session", path="/")
    response.delete_cookie("controlhub_csrf", path="/")
    return response
