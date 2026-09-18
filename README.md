# ControlHub

Centro de control personal para organizar, consultar y gestionar recursos de infraestructura y servicios digitales desde una única interfaz.

## Estado del proyecto

ControlHub dispone de una base funcional con autenticación, dashboard inicial y gestión de recursos en desarrollo. La rama de trabajo todavía no se ha fusionado.

## V1

La V1 incluye progresivamente:

- dashboard;
- recursos y tarjetas;
- categorías;
- tags;
- favoritos;
- búsqueda;
- URLs;
- información SSH y copia de comandos;
- autenticación;
- panel de administración;
- auditoría;
- interfaz responsive/mobile-first.

Los secretos se mantendrán separados del modelo normal de recursos. No se ejecutarán comandos remotos arbitrarios desde la interfaz.

## Producción

Apache HTTPS
    |
Uvicorn/systemd
    |
FastAPI
    |
SQLite

El backend escucha únicamente en loopback. El puerto interno actual es 8008.

La documentación de desarrollo y operación se encuentra en docs/DEVELOPMENT.md.

## Documentación

- docs/ARCHITECTURE.md
- docs/ROADMAP.md
- docs/DEVELOPMENT.md
- docs/PROJECT-STATE.md
- docs/DECISIONS.md
- CHANGELOG.md
