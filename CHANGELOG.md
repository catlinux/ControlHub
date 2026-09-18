# Changelog

Todos los cambios relevantes de ControlHub se documentarán en este archivo.

## [Unreleased]

### Añadido

- Primera base funcional de autenticación con sesiones server-side.
- Rol administrativo inicial.
- Panel web mínimo.
- Botón administrativo para solicitar el reinicio de `controlhub.service`.
- Protección CSRF para las acciones de sesión y administración.
- Auditoría mínima de login, logout y solicitudes de reinicio.
- Servicio del frontend compilado desde FastAPI.
- Documentación de instalación y operación del servicio systemd.
- Documentación de la regla sudoers de mínimo privilegio.

### Cambiado

- El backend sirve el frontend compilado cuando existe `frontend/dist`.
- La inicialización de la aplicación utiliza el ciclo de vida `lifespan` de FastAPI.
- CI deja de depender de un `package-lock.json` inexistente.

### Corregido

- Formato Python incompatible con Ruff en los nuevos módulos y tests.
- Cierre de sesión sin protección CSRF.
- Artefactos `*.egg-info` añadidos a las exclusiones de Git.

### Pendiente

- Migrar la persistencia inicial de autenticación de `sqlite3` a SQLModel/Alembic.
- Incorporar rate limiting para endpoints sensibles.
