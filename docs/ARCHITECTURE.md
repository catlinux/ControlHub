# Arquitectura

## 1. Objetivo

La arquitectura de ControlHub proporciona una base sencilla para un centro de control personal extensible, evitando microservicios y complejidad distribuida mientras no exista una necesidad real.

## 2. Enfoque

La V1 utiliza un monolito modular:

Apache HTTPS
    |
Uvicorn / systemd
    |
FastAPI
    |-- autenticación/autorización
    |-- recursos
    |-- administración
    |-- secretos
    |
SQLModel
    |
SQLite + Alembic

## 3. Stack

- Backend: Python + FastAPI + SQLModel + Uvicorn.
- Migraciones: Alembic.
- Frontend: Vue 3 + TypeScript.
- Persistencia V1: SQLite.
- API REST versionada bajo /api/v1.
- Producción: Apache HTTPS -> Uvicorn/systemd -> FastAPI -> SQLite.
- V1 sin Docker.

## 4. Estructura

- app/api: endpoints HTTP.
- app/auth: autenticación y sesiones.
- app/models: modelos persistentes.
- app/security: controles de seguridad.
- app/secrets.py: cifrado mediante Fernet.
- app/db.py: motor, sesiones y arranque de migraciones.
- app/services: lógica de negocio que se vaya extrayendo.
- frontend: interfaz Vue.
- docs: documentación y decisiones.
- migrations: scripts de Alembic para evolución del esquema.

## 5. Modelo de recursos

Resource es la entidad central de la V1.

Incluye:

- identidad: nombre, descripción y tipo;
- organización: categoría, tags y favorito;
- conexión: URL, host, puerto y usuario;
- presentación: icono y estado;
- notas y metadatos específicos.

Relaciones:

Category 1 -> N Resource
Resource N -> N Tag

Las contraseñas, tokens, claves privadas y otros secretos no forman parte de Resource.

## 6. Secretos

Secret es una entidad separada que almacena únicamente un valor cifrado.

- Cifrado: Fernet de cryptography.
- Clave: CONTROLHUB_SECRET_KEY, fuera del repositorio y de la base de datos.
- La API de listado devuelve sólo metadatos.
- Las operaciones están limitadas a administración.
- No se implementa criptografía propia.

## 7. API

Los recursos exponen inicialmente:

- GET /api/v1/resources
- GET /api/v1/resources/{id}
- POST /api/v1/resources
- PUT /api/v1/resources/{id}
- PATCH /api/v1/resources/{id}/favorite
- DELETE /api/v1/resources/{id}
- GET /api/v1/categories
- POST /api/v1/categories
- DELETE /api/v1/categories/{id}
- GET /api/v1/tags

Administración:

- GET/POST /api/v1/admin/users
- PATCH /api/v1/admin/users/{id}/role
- PATCH /api/v1/admin/users/{id}/password
- DELETE /api/v1/admin/users/{id}
- GET /api/v1/admin/audit
- POST /api/v1/admin/restart

Secretos:

- GET/POST /api/v1/secrets
- PUT/DELETE /api/v1/secrets/{id}

La búsqueda se realiza mediante filtros de API. El frontend nunca accede directamente a SQLite.

## 8. Seguridad

La autenticación utiliza sesiones server-side, cookies HttpOnly/Secure/SameSite y Argon2id. Las mutaciones requieren CSRF.

Los endpoints sensibles incorporan rate limiting en memoria, adecuado al despliegue V1 de un único proceso.

La acción administrativa de reinicio está limitada a una orden exacta de systemd mediante sudoers de mínimo privilegio. ControlHub no ejecuta comandos remotos arbitrarios.

## 9. Testing

Backend: pytest + Ruff. Frontend: Vitest + ESLint + build. Los flujos de navegador se cubrirán progresivamente con Playwright.

## 10. Internacionalización y accesibilidad

El software empieza en castellano. La arquitectura evita acoplar de forma irreversible los textos a la lógica para permitir i18n futura. La interfaz debe mantener controles accesibles y usable en móvil.
