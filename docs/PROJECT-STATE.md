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
- Protección CSRF para la acción administrativa.
- Auditoría mínima de solicitudes de reinicio.
- El servicio de producción utiliza el puerto interno configurable 8008.

## Integración pendiente en Debian

El entorno existente puede conservar `CONTROLHUB_HOST=127.0.0.1` y `CONTROLHUB_PORT=8008`.

Hay que añadir al entorno de producción las credenciales iniciales del administrador y, para habilitar el botón, una regla sudoers exacta que permita únicamente reiniciar `controlhub.service`.

El frontend debe compilarse antes de poner esta versión detrás de Apache.

## Próximo paso

Integrar esta versión en Debian, construir el frontend, crear/ajustar el usuario administrador y verificar login → panel → reinicio → recuperación. Después continuar con el modelo funcional de recursos y la migración de base de datos prevista para V1.
