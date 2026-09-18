# ControlHub

Centro de control personal para organizar, consultar y gestionar recursos de infraestructura y servicios digitales desde una única interfaz.

## Estado del proyecto

ControlHub dispone de una primera base funcional ejecutable con autenticación, panel inicial y una acción administrativa controlada para reiniciar el servicio de la aplicación.

## V1

La V1 incluirá dashboard, recursos, categorías, tags, favoritos, búsqueda, información SSH, autenticación, panel de administración integrado, gestión de secretos cifrados, auditoría e interfaz responsive/mobile-first. La arquitectura quedará preparada para internacionalización futura.

La V1 no ejecutará comandos remotos arbitrarios ni incorporará monitorización avanzada sin una necesidad concreta.

## Producción

```text
Apache HTTPS
    ↓
Uvicorn/systemd
    ↓
FastAPI
    ↓
SQLite
```

El backend escucha únicamente en loopback. El puerto interno actual es 8008 y se configura mediante el entorno.

La documentación de despliegue y operación se encuentra en [Desarrollo](docs/DEVELOPMENT.md).

## Documentación

- [Arquitectura](docs/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)
- [Desarrollo](docs/DEVELOPMENT.md)
- [Estado del proyecto](docs/PROJECT-STATE.md)
- [Registro de decisiones](docs/DECISIONS.md)
- [Changelog](CHANGELOG.md)
