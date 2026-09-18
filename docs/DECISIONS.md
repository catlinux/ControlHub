# Decisiones técnicas

Registro de decisiones importantes del proyecto.

## DEC-001 — Monolito modular para la V1

**Estado:** Aceptada

La V1 utilizará un monolito modular en lugar de microservicios. La aplicación mantiene separación interna clara entre presentación, API, lógica, persistencia, autenticación e integraciones.

## DEC-002 — Los secretos quedan fuera del modelo normal de recursos

**Estado:** Aceptada

Contraseñas, tokens, claves privadas y otros secretos no se almacenarán como campos normales de Resource.

## DEC-003 — Documentación en castellano

**Estado:** Aceptada

README, documentación técnica, roadmap, changelog y documentos del proyecto se mantienen en castellano.

## DEC-004 — Backend Python + FastAPI

**Estado:** Aceptada

El backend utiliza Python + FastAPI.

## DEC-005 — Frontend Vue 3 + TypeScript

**Estado:** Aceptada

El frontend utiliza Vue 3 + TypeScript. Las dependencias adicionales sólo se incorporarán cuando aporten valor real.

## DEC-006 — SQLite + SQLModel + Alembic

**Estado:** Aceptada

La V1 utiliza SQLite y SQLModel. Alembic será el mecanismo único para evolucionar el esquema antes de ampliar de nuevo el modelo de datos.

## DEC-007 — Sesiones server-side y Argon2id

**Estado:** Aceptada

La autenticación utiliza sesiones gestionadas por servidor mediante cookies seguras. Las contraseñas se almacenan con Argon2id.

## DEC-008 — Secretos cifrados y separados

**Estado:** Aceptada

Los secretos se almacenarán cifrados en un subsistema separado del modelo Resource. La clave de cifrado permanecerá fuera de la base de datos y del repositorio. No se implementará criptografía propia.

## DEC-009 — Panel de administración integrado

**Estado:** Aceptada

La administración forma parte de la V1 e incluirá recursos, categorías, tags, usuarios, roles/permisos, secretos, auditoría y configuración.

## DEC-010 — Producción con Apache + systemd

**Estado:** Aceptada

La V1 se despliega sin Docker: Apache HTTPS -> Uvicorn gestionado por systemd -> FastAPI -> SQLite. FastAPI escucha únicamente en loopback.

## DEC-011 — API REST versionada

**Estado:** Aceptada

Frontend y backend se comunican mediante REST bajo /api/v1. El navegador nunca accede directamente a SQLite.

## DEC-012 — Testing y CI

**Estado:** Aceptada

Se utilizan pytest, Vitest y GitHub Actions. Los flujos de navegador se cubrirán progresivamente con Playwright. No habrá despliegue automático a producción en V1.

## DEC-013 — Sin ejecución remota arbitraria en V1

**Estado:** Aceptada

ControlHub no ejecutará comandos remotos arbitrarios desde acciones de interfaz. Las acciones futuras requerirán un modelo explícito de permisos y ejecución segura.

## DEC-014 — Estado técnico consolidado antes de implementar

**Estado:** Aceptada

Las decisiones principales de arquitectura deben quedar documentadas y verificadas antes de ampliar la implementación.

## DEC-015 — Configuración de producción fuera del repositorio

**Estado:** Aceptada

La configuración de producción y los secretos se mantienen en /etc/controlhub/controlhub.env, fuera del árbol de código. Esto separa despliegue, código y secretos sin introducir un gestor de secretos externo en la V1.

## DEC-016 — Resource como entidad central de V1

**Estado:** Aceptada

Resource será la entidad central del dashboard. Categorías y tags proporcionan organización transversal, mientras que los datos específicos del tipo se mantienen en campos y metadatos del recurso.

## DEC-017 — No versionar package-lock por ahora

**Estado:** Provisional

El repositorio no versionará actualmente frontend/package-lock.json. La política podrá revisarse si se decide adoptar instalaciones reproducibles mediante npm ci.


## DEC-018 — Rate limiting en memoria para V1

**Estado:** Aceptada

La V1 utiliza un limitador en memoria para reducir intentos automatizados contra endpoints sensibles. Es suficiente para el despliegue inicial de un único proceso y no se considera un mecanismo distribuido.

## DEC-019 — Cifrado Fernet para secretos

**Estado:** Aceptada

Los secretos se cifran mediante Fernet de la biblioteca cryptography. La clave se proporciona mediante CONTROLHUB_SECRET_KEY y permanece fuera del repositorio y de la base de datos. La API no devuelve el valor ni el ciphertext.

## DEC-020 — Administración integrada en V1

**Estado:** Aceptada

La administración de la V1 permite gestionar usuarios, roles, contraseñas, secretos y consultar auditoría. Las acciones administrativas siguen protegidas por autenticación, CSRF y rate limiting cuando corresponde.
