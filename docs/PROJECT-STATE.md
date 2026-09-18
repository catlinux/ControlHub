# Estado del proyecto

**Fecha de referencia:** 2026-09-18

## Estado general

ControlHub está pasando de la base de autenticación al dashboard funcional de la V1. El despliegue existente en Debian continúa operativo con Apache HTTPS -> Uvicorn/systemd -> FastAPI -> SQLite.

## Repositorio

- Repositorio: catlinux/ControlHub.
- Rama de trabajo: feature/admin-restart.
- PR #1: abierto y en estado draft; no debe fusionarse todavía.
- La última versión previamente verificada por CI fue el commit 31e05a36a3e6963e2b11c464711c53cd7cc3f264.
- La rama actual ya contiene el primer bloque de recursos y el dashboard asociado; el nuevo CI está en ejecución y debe quedar verde antes del despliegue.

## Producción Debian

- Usuario de servicio: stark.
- Aplicación: /opt/controlhub.
- Backend: 127.0.0.1:8008.
- Apache publica https://hub.warcrafted.com.
- Certificado HTTPS operativo y renovación automática configurada.
- Configuración de producción: /etc/controlhub/controlhub.env.
- Servicio: controlhub.service, habilitado y activo.
- Sudoers permite exclusivamente /bin/systemctl restart controlhub.service.
- Verificado en servidor: health local y health HTTPS devuelven {"status":"ok"}.
- El servidor todavía ejecuta la versión anterior; no se debe desplegar el nuevo dashboard hasta completar CI y las pruebas locales.

## Funcionalidad implementada en la rama

- Autenticación con sesiones server-side.
- Argon2id para contraseñas.
- Protección CSRF.
- Auditoría básica.
- Reinicio administrativo seguro y limitado.
- Persistencia común mediante SQLModel.
- Entidades User, sesión, auditoría, Category, Tag y Resource.
- CRUD inicial de recursos.
- Búsqueda por nombre, descripción, host y URL.
- Filtro por categoría y favoritos.
- Tags asociados a recursos.
- URLs y datos SSH.
- Copia de comandos SSH desde el dashboard.
- Interfaz responsive inicial para tarjetas de recursos.

## Deuda técnica y seguridad

- Alembic todavía debe consolidarse como mecanismo único de migraciones.
- Rate limiting de login y otros endpoints sensibles sigue pendiente.
- El sistema de secretos cifrados separado del modelo Resource sigue pendiente.
- La gestión avanzada de usuarios, roles y permisos sigue pendiente.
- Los estados de recursos todavía son informativos; no hay monitorización activa.
- Deben añadirse pruebas de integración y Playwright progresivamente.
- Debe revisarse la política de frontend/package-lock.json antes de adoptar npm ci.

## Siguiente bloque de trabajo

1. Dejar CI verde para el bloque de recursos.
2. Actualizar y verificar el servidor.
3. Consolidar Alembic.
4. Completar gestión de categorías y tags desde la interfaz.
5. Añadir rate limiting y pruebas de integración.
6. Continuar con estados básicos, administración y secretos según el orden de la V1.
