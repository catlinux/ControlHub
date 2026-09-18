# Estado del proyecto

**Fecha de referencia:** 2026-09-18

## Estado general

ControlHub está en fase de arquitectura técnica consolidada, antes de la implementación funcional.

## Repositorio

- Repositorio GitHub creado.
- Visibilidad: pública.
- Organización/propietario: Catlinux.
- Todavía no se ha realizado la implementación inicial.

## Decisiones confirmadas

- El proyecto se denomina ControlHub.
- La documentación y las descripciones del proyecto se redactarán en castellano.
- El software comenzará en castellano.
- La arquitectura se preparará para internacionalización futura.
- La V1 priorizará simplicidad, seguridad, fiabilidad y mantenibilidad.
- Se evitará la complejidad innecesaria.
- Las credenciales y secretos estarán separados del modelo normal de recursos.
- El proyecto utilizará Git desde el principio.
- Se seguirá la metodología INSPECT → PLAN → EXECUTE → VERIFY → DOCUMENT → BACKUP.

## Decisiones técnicas consolidadas

- Monolito modular y monorepo.
- Backend Python + FastAPI.
- Frontend Vue 3 + TypeScript + Tailwind CSS.
- SQLite + SQLModel + Alembic.
- REST /api/v1.
- Sesiones server-side + Argon2id.
- Secretos separados y cifrados.
- User → Role → Permission.
- Panel de administración integrado en V1.
- Auditoría y logs separados.
- Apache + Uvicorn/systemd + FastAPI en producción.
- Sin Docker en V1.
- pytest, Vitest, Playwright y GitHub Actions.

## Pendiente de decidir

- Diseño detallado del modelo de datos, antes de crear la migración inicial.
- Detalle final de la UI y navegación, validado durante el prototipo.

## Próximo paso

Crear la estructura inicial del monorepo y el esqueleto mínimo de frontend, backend, tests, scripts y configuración.
