# ControlHub

Centro de control personal para organizar, consultar y gestionar recursos de infraestructura y servicios digitales desde una única interfaz.

## Estado del proyecto

ControlHub se encuentra en fase de arquitectura técnica consolidada, antes de la implementación funcional.

## V1

La V1 incluirá dashboard, recursos, categorías, tags, favoritos, búsqueda, información SSH, autenticación, panel de administración integrado, gestión de secretos cifrados, auditoría e interfaz responsive/mobile-first. La arquitectura quedará preparada para internacionalización futura.

La V1 no ejecutará comandos remotos arbitrarios ni incorporará monitorización avanzada sin una necesidad concreta.

## V1 definida

La V1 incluirá dashboard, recursos, categorías, tags, favoritos, búsqueda, información SSH, autenticación, panel de administración integrado, gestión de secretos cifrados, auditoría e interfaz responsive/mobile-first.

La V1 no ejecutará comandos remotos arbitrarios ni incorporará monitorización avanzada sin una necesidad concreta.

## Objetivos

ControlHub está diseñado para centralizar el acceso y la información de diferentes recursos digitales, entre ellos:

- Sitios web y aplicaciones web
- Servidores y VPS
- Conexiones SSH
- Servicios
- Repositorios Git
- Bases de datos
- Herramientas de administración
- Servicios cloud
- Sistemas de monitorización
- Backups
- Documentación

La aplicación debe mantener una arquitectura sencilla y mantenible, pero preparada para incorporar nuevos tipos de recursos e integraciones en el futuro.

## Principios

1. Simplicidad
2. Seguridad
3. Fiabilidad
4. Mantenibilidad
5. Arquitectura extensible
6. Buena experiencia de usuario, especialmente en dispositivos móviles
7. Evitar dependencias innecesarias
8. No implementar funcionalidades únicamente porque sean posibles
9. Evitar duplicar servicios o componentes sin una razón clara
10. Documentar las decisiones importantes

## Metodología

Los cambios importantes seguirán este flujo:

**INSPECT → PLAN → EXECUTE → VERIFY → DOCUMENT → BACKUP**

## Documentación

- [Arquitectura](docs/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)
- [Desarrollo](docs/DEVELOPMENT.md)
- [Estado del proyecto](docs/PROJECT-STATE.md)
- [Registro de decisiones](docs/DECISIONS.md)
- [Changelog](CHANGELOG.md)

## Licencia

ControlHub se distribuirá bajo la licencia MIT, salvo que una decisión posterior del proyecto establezca lo contrario.
