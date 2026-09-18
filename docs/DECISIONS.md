# Decisiones técnicas

Registro de decisiones importantes del proyecto.

## DEC-001 — Monolito modular para la V1

**Estado:** Aceptada

### Decisión

La primera versión de ControlHub utilizará un enfoque de monolito modular en lugar de una arquitectura basada en microservicios.

### Motivo

La V1 no necesita la complejidad operativa de una arquitectura distribuida. Un monolito modular permite mantener una estructura clara y facilita la evolución posterior.

### Consecuencia

La aplicación deberá mantener una separación interna clara entre presentación, API, lógica de negocio, persistencia, autenticación e integraciones.

## DEC-002 — Los secretos quedan fuera del modelo normal de recursos

**Estado:** Aceptada

### Decisión

Contraseñas, tokens, claves privadas y otros secretos no se almacenarán como campos normales de `Resource`.

### Motivo

Reduce el impacto de una posible exposición de la base de datos y permite diseñar posteriormente un mecanismo específico de gestión de secretos.

### Consecuencia

Los recursos podrán contener referencias o datos de conexión no sensibles, mientras que los secretos se gestionarán de forma separada.

## DEC-003 — Documentación en castellano

**Estado:** Aceptada

### Decisión

La documentación y las descripciones del proyecto se redactarán en castellano.

### Consecuencia

README, documentación técnica, roadmap, changelog y documentos del proyecto deberán mantenerse en castellano.


## DEC-004 — Backend Python + FastAPI

**Estado:** Aceptada

El backend utilizará Python + FastAPI.

## DEC-005 — Frontend Vue 3 + TypeScript

**Estado:** Aceptada

El frontend utilizará Vue 3 + TypeScript, Tailwind CSS, componentes propios, Pinia cuando aporte valor y Vue I18n desde V1.

## DEC-006 — SQLite + SQLModel + Alembic

**Estado:** Aceptada

La V1 utilizará SQLite, SQLModel para el modelado y Alembic para migraciones. La persistencia no deberá bloquear una futura migración a PostgreSQL si fuese necesaria.

## DEC-007 — Sesiones server-side y Argon2id

**Estado:** Aceptada

La autenticación utilizará sesiones gestionadas por servidor mediante cookies seguras. Las contraseñas se almacenarán con Argon2id. El modelo de autorización será User → Role → Permission.

## DEC-008 — Secretos cifrados y separados

**Estado:** Aceptada

Los secretos se almacenarán cifrados en un subsistema separado del modelo Resource. La clave de cifrado se mantendrá fuera de la base de datos y del repositorio. No se implementará criptografía propia.

## DEC-009 — Panel de administración integrado

**Estado:** Aceptada

La administración forma parte de la V1 e incluirá recursos, categorías, tags, usuarios, roles/permisos, secretos, auditoría y configuración.

## DEC-010 — Producción con Apache + systemd

**Estado:** Aceptada

La V1 se desplegará sin Docker: Apache HTTPS → Uvicorn gestionado por systemd → FastAPI → SQLite. FastAPI escuchará únicamente en loopback.

## DEC-011 — API REST versionada

**Estado:** Aceptada

Frontend y backend se comunicarán mediante REST bajo /api/v1. El navegador nunca accederá directamente a SQLite.

## DEC-012 — Testing y CI

**Estado:** Aceptada

Se utilizarán pytest, Vitest y Playwright. GitHub Actions ejecutará lint, tests, build y comprobaciones de calidad. No habrá despliegue automático a producción en V1.

## DEC-013 — Sin ejecución remota arbitraria en V1

**Estado:** Aceptada

ControlHub no ejecutará comandos remotos arbitrarios desde acciones de interfaz. Las acciones remotas futuras requerirán un modelo explícito de permisos y ejecución segura.

## DEC-014 — Estado técnico consolidado antes de implementar

**Estado:** Aceptada

La documentación y las decisiones principales de arquitectura deben quedar consolidadas antes de crear la implementación funcional.
