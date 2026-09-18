# Changelog

Todos los cambios relevantes de ControlHub se documentarán en este archivo.

## [Unreleased]

### Añadido

- Primera base funcional de autenticación con sesiones server-side.
- Rol administrativo inicial.
- Panel web mínimo.
- Botón administrativo para solicitar el reinicio de `controlhub.service`.
- Protección CSRF para la acción administrativa.
- Auditoría mínima de solicitudes de reinicio.
- Servicio del frontend compilado desde FastAPI.
- Documentación de instalación y operación del servicio systemd.
- Documentación de la regla sudoers de mínimo privilegio.

### Cambiado

- El backend sirve el frontend compilado cuando existe `frontend/dist`.

### Corregido

- Ninguno.
