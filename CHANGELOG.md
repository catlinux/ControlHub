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
- Persistencia común mediante SQLModel.
- Entidades Category, Tag y Resource.
- CRUD inicial de recursos.
- Búsqueda y filtros por categoría/favoritos.
- URLs, host, puerto, usuario y copia de comandos SSH.
- Dashboard inicial basado en tarjetas de recursos.

### Cambiado

- La persistencia de autenticación deja de utilizar conexiones sqlite3 directas y pasa por SQLModel.
- El frontend pasa de ser únicamente un panel administrativo a mostrar el dashboard de recursos.
- La configuración de producción se mantiene fuera del repositorio en /etc/controlhub/controlhub.env.

### Corregido

- Artefactos __pycache__ quedan excluidos del repositorio.
- Carga de los modelos SQLModel al iniciar FastAPI para registrar el esquema común.

### Pendiente

- Consolidar Alembic como mecanismo de migración de esquema.
- Incorporar rate limiting para endpoints sensibles.
- Implementar gestión cifrada de secretos separada de Resource.
- Completar administración de categorías/tags, usuarios, roles y auditoría.
- Mejorar estados básicos de recursos sin convertirlos todavía en monitorización avanzada.
- Añadir pruebas de integración y navegador.
