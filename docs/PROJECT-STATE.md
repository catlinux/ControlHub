# Estado del proyecto

**Fecha de referencia:** 2026-09-18

## Estado general

ControlHub dispone de una base funcional de la V1 en la rama `feature/admin-restart`. El despliegue existente en Debian está operativo con Apache HTTPS -> Uvicorn/systemd -> FastAPI -> SQLite.

## Repositorio

- Repositorio: catlinux/ControlHub.
- Rama de trabajo: feature/admin-restart.
- PR #1: abierto y en estado draft; no debe fusionarse todavía.
- La rama contiene autenticación, portal, recursos, administración, seguridad y migraciones de la V1.
- CI del bloque actual: frontend y backend correctos.

## Producción Debian

- Usuario de servicio: stark.
- Aplicación: /opt/controlhub.
- Backend: 127.0.0.1:8008.
- Apache publica https://hub.warcrafted.com.
- Certificado HTTPS operativo y renovación automática configurada.
- Configuración de producción: /etc/controlhub/controlhub.env.
- Servicio: controlhub.service, habilitado y activo.
- Sudoers permite exclusivamente /bin/systemctl restart controlhub.service.
- Verificado previamente en servidor: health local y health HTTPS devuelven {"status":"ok"}.
- El bloque actual todavía requiere despliegue controlado en Debian.

## Funcionalidad implementada en la rama

- Autenticación con sesiones server-side y Argon2id.
- Protección CSRF.
- Rate limiting básico para login y acciones administrativas.
- Auditoría básica.
- Reinicio administrativo seguro y limitado.
- Persistencia mediante SQLModel.
- Alembic como mecanismo único de evolución de esquema.
- Entidades User, sesión, auditoría, Category, Tag, Resource y Secret.
- Lectura de recursos para usuarios autenticados.
- Gestión de recursos y categorías restringida a administradores.
- Búsqueda por nombre, descripción, host y URL.
- Filtros por categoría, favoritos y tags.
- URLs y datos SSH.
- Copia de comandos SSH.
- Portal responsive con tarjetas y agrupación por categoría.
- Administración en modal con usuarios, secretos, auditoría y sistema.
- Almacén de secretos cifrados separado del modelo Resource.
- Protección contra indexación mediante meta robots, X-Robots-Tag y robots.txt.

## Deuda técnica y seguridad

- CONTROLHUB_SECRET_KEY debe configurarse en producción antes de utilizar secretos.
- Los estados de recursos todavía son informativos; no hay monitorización activa.
- Deben añadirse pruebas de navegador y una verificación E2E del despliegue.
- Debe completarse la revisión final de accesibilidad y contratos OpenAPI.
- La política de frontend/package-lock.json continúa siendo no versionarlo por ahora.

## Siguiente bloque de trabajo

1. Desplegar controladamente la rama en Debian.
2. Verificar la experiencia real del portal con los recursos existentes.
3. Configurar y verificar CONTROLHUB_SECRET_KEY fuera del repositorio.
4. Ejecutar pruebas de integración y navegador.
5. Completar estados técnicos básicos y revisión final de la V1.
6. Actualizar documentación y dejar el PR listo para revisión, sin fusionarlo automáticamente.
