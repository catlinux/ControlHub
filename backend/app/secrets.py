from __future__ import annotations

import os

from cryptography.fernet import Fernet, InvalidToken


class SecretStoreError(RuntimeError):
    pass


def _fernet() -> Fernet:
    key = os.getenv("CONTROLHUB_SECRET_KEY", "").strip()
    if not key:
        raise SecretStoreError("CONTROLHUB_SECRET_KEY no está configurada.")
    try:
        return Fernet(key.encode())
    except ValueError as exc:
        raise SecretStoreError("CONTROLHUB_SECRET_KEY no es una clave Fernet válida.") from exc


def encrypt(value: str) -> str:
    return _fernet().encrypt(value.encode()).decode()


def decrypt(value: str) -> str:
    try:
        return _fernet().decrypt(value.encode()).decode()
    except InvalidToken as exc:
        raise SecretStoreError("No se pudo descifrar el secreto.") from exc
