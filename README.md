# ControlHub

Centro de control personal para organizar, consultar y gestionar recursos de infraestructura y servicios digitales desde una única interfaz.

## Estado del proyecto

ControlHub dispone de una base funcional de la V1 con autenticación, dashboard, recursos, administración, auditoría, migraciones y almacenamiento cifrado de secretos. La rama de trabajo todavía no se ha fusionado.

## V1

La V1 incluye:

- dashboard;
- recursos y tarjetas;
- categorías y tags;
- búsqueda y filtros;
- favoritos;
- URLs;
- información SSH y copia de comandos;
- autenticación;
- panel de administración;
- usuarios y roles básicos;
- secretos cifrados separados de Resource;
- auditoría;
- rate limiting básico;
- interfaz responsive/mobile-first.

Los secretos se mantienen separados del modelo normal de recursos. No se ejecutan comandos remotos arbitrarios desde la interfaz.

## Producción

Apache HTTPS
    |
Uvicorn/systemd
    |
FastAPI
    |
SQLite + Alembic

El backend escucha únicamente en loopback. El puerto interno actual es 8008.

La configuración de producción se mantiene en /etc/controlhub/controlhub.env y nunca se introduce en Git.

La documentación de desarrollo y operación se encuentra en docs/DEVELOPMENT.md.

## Documentación

- docs/ARCHITECTURE.md
- docs/ROADMAP.md
- docs/DEVELOPMENT.md
- docs/PROJECT-STATE.md
- docs/DECISIONS.md
- CHANGELOG.md


## Privacidad e indexación

ControlHub es un centro de control privado y no un sitio público. La aplicación requiere autenticación para acceder al portal y a los recursos y aplica noindex mediante meta robots y cabecera X-Robots-Tag. También publica un robots.txt que bloquea el rastreo y no mantiene sitemap.

La administración está separada visualmente del portal y sólo está disponible para usuarios con rol administrador. Los usuarios normales utilizan ControlHub como portal de acceso a los recursos autorizados.

La no indexación no sustituye a la autenticación, autorización ni al resto de controles de seguridad.
