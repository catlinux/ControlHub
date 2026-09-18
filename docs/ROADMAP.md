# Roadmap

Este roadmap es orientativo. Las funcionalidades futuras no se consideran obligatorias hasta que exista una necesidad concreta.

## V1 — Centro de control funcional

### Implementado en la rama actual

- Dashboard.
- Recursos y tarjetas.
- Categorías y tags.
- Búsqueda y filtros.
- Favoritos.
- URLs.
- Información SSH y copia de comandos.
- Autenticación con sesiones server-side.
- Protección CSRF.
- Rate limiting básico para login y acciones administrativas sensibles.
- Panel de administración integrado.
- Gestión básica de usuarios, roles y contraseñas.
- Gestión de secretos cifrados separada de Resource.
- Auditoría consultable.
- Persistencia SQLModel con Alembic.
- Interfaz responsive/mobile-first.
- API REST bajo /api/v1.
- Despliegue preparado con Apache HTTPS -> Uvicorn/systemd -> FastAPI -> SQLite.

### Pendiente de completar la V1

- Estados técnicos activos online/offline/warning sin convertirlos todavía en monitorización avanzada.
- Pruebas de navegador con Playwright y verificación E2E del despliegue.
- Revisión final de accesibilidad y experiencia móvil.
- Revisión de OpenAPI y contratos de API.
- Validación final de recuperación y documentación operativa.
- Configuración de CONTROLHUB_SECRET_KEY en producción antes de utilizar secretos cifrados.

### No incluido inicialmente

- Ejecución remota arbitraria.
- Monitorización avanzada.
- Integraciones externas complejas.
- Automatizaciones complejas.

## V2 — Supervisión

Posibles funcionalidades:

- Monitorización.
- Estado de servicios.
- Comprobación SSL.
- Información de backups.
- Inventario de infraestructura.
- Documentación asociada.

## V3 — Integraciones y acciones

Posibles funcionalidades:

- Integración con GitHub.
- Integración con sistemas de backup.
- Monitorización avanzada.
- Notificaciones.
- API pública o privada.
- Roles y permisos avanzados.
- Acciones remotas controladas.

Las fases podrán modificarse según las necesidades reales.


## Experiencia de uso de la V1

- Portal privado como pantalla principal.
- Recursos agrupados visualmente por categoría.
- Favoritos, búsqueda y filtros.
- Administración separada del portal mediante modal.
- Administración organizada en usuarios, secretos, auditoría y sistema.
- Gestión de recursos y categorías restringida al rol administrador.

## Privacidad

- Aplicación no indexable por buscadores.
- Meta robots y cabecera X-Robots-Tag.
- robots.txt sin sitemap.
