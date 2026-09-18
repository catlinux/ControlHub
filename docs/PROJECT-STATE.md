# Estado del proyecto

**Fecha de referencia:** 2026-09-18

## Estado general

ControlHub ya dispone de una base funcional ejecutable y está avanzando sobre la V1 real. El despliegue de la aplicación en el Debian doméstico está operativo mediante Apache HTTPS -> Uvicorn/systemd -> FastAPI -> SQLite.

## Repositorio

- Repositorio: catlinux/ControlHub.
- Rama de trabajo: feature/admin-restart.
- PR #1: abierto y en estado draft; no debe fusionarse todavía.
- CI del commit 31e05a36a3e6963e2b11c464711c53cd7cc3f264: backend y frontend correctos.
- La rama contiene autenticación, sesión, CSRF, auditoría y reinicio administrativo.
- La siguiente etapa de implementación es el modelo funcional de recursos de la V1.

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

## Funcionalidad implementada

- Autenticación con sesiones server-side.
- Argon2id para contraseñas.
- Protección CSRF.
- Auditoría básica.
- Panel web responsive.
- Reinicio administrativo seguro y limitado.

## Deuda técnica y seguridad

- La persistencia inicial de autenticación sigue utilizando sqlite3 directo; antes de ampliar el modelo de recursos debe migrarse al modelo SQLModel común.
- Rate limiting de login y otros endpoints sensibles sigue pendiente.
- El sistema de secretos cifrados separado del modelo Resource sigue pendiente.
- La gestión avanzada de roles/permisos sigue pendiente.
- La comprobación de estado de recursos todavía no ejecuta monitorización activa.
- Alembic debe quedar establecido para las migraciones de esquema antes de ampliar más el modelo.
- Deben añadirse pruebas de integración y Playwright progresivamente.

## Entorno local

Tras ejecutar npm install, el entorno local puede generar frontend/package-lock.json. El repositorio actual no lo versiona; no debe añadirse automáticamente sin una decisión explícita sobre la política de lockfiles del proyecto.

## Siguiente bloque de trabajo

1. Consolidar SQLModel/Alembic para la persistencia común.
2. Implementar Resource, Category y Tag.
3. Implementar dashboard, búsqueda, favoritos, URL y SSH.
4. Verificar CI y desplegar.
5. Añadir rate limiting y pruebas de integración.
