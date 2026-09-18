# Estado del proyecto

**Fecha de referencia:** 2026-09-18

## Estado general

ControlHub ha pasado del esqueleto técnico a una primera base funcional ejecutable.

## Estado actual

- Backend FastAPI ejecutable mediante Uvicorn/systemd.
- Frontend Vue 3 + TypeScript.
- Autenticación inicial con sesiones server-side almacenadas en SQLite.
- Rol administrativo inicial.
- Panel web mínimo.
- Acción administrativa `Reiniciar ControlHub`.
- Protección CSRF para las acciones de sesión y administración.
- Auditoría mínima de login, logout y solicitudes de reinicio.
- El servicio de producción utiliza el puerto interno configurable 8008.
- El frontend compilado puede ser servido por FastAPI detrás de Apache.

## Integración pendiente en Debian

El entorno existente puede conservar `CONTROLHUB_HOST=127.0.0.1` y `CONTROLHUB_PORT=8008`.

Hay que añadir al entorno de producción las credenciales iniciales del administrador y, para habilitar el botón, una regla sudoers exacta que permita únicamente reiniciar `controlhub.service`.

El frontend debe compilarse antes de poner esta versión detrás de Apache.

## Deuda técnica conocida

La autenticación inicial utiliza directamente `sqlite3` como implementación transitoria del prototipo. La decisión arquitectónica de V1 sigue siendo SQLite + SQLModel + Alembic; antes de ampliar el modelo funcional de recursos se deberá migrar esta persistencia al modelo común y crear la migración Alembic correspondiente.

También queda pendiente incorporar rate limiting para endpoints sensibles antes de considerar la autenticación lista para producción.

## Próximo paso

Integrar esta versión en Debian, construir el frontend y verificar login → panel → reinicio → recuperación. Después completar el modelo SQLModel/Alembic y comenzar el modelo funcional de recursos de V1.
