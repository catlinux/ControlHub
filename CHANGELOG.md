# Changelog

Todos los cambios relevantes de ControlHub se documentarán en este archivo.

## [Unreleased]

### Añadido

- Primera base funcional de autenticación con sesiones server-side.
- Rol administrativo inicial.
- Panel web responsive.
- Botón administrativo para reiniciar controlhub.service.
- Protección CSRF para las acciones de sesión y administración.
- Auditoría mínima de login, logout y acciones administrativas.

### Cambiado

- El siguiente bloque de desarrollo pasa a centrarse en el modelo funcional de recursos de V1.
- La configuración de producción se mantiene fuera del repositorio en /etc/controlhub/controlhub.env.

### Corregido

- Artefactos __pycache__ quedan excluidos del repositorio.

### Pendiente

- Migrar la persistencia de autenticación a SQLModel/Alembic.
- Implementar Resource, Category y Tag.
- Implementar dashboard, búsqueda, favoritos, URL y SSH.
- Incorporar rate limiting para endpoints sensibles.
- Implementar gestión cifrada de secretos separada de Resource.
