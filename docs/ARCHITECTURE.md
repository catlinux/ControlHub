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
    |-- servicios
    |
SQLModel
    |
SQLite

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
- app/db.py: motor y sesiones de base de datos.
- app/services: lógica de negocio que se vaya extrayendo.
- app/security: controles de seguridad específicos.
- frontend: interfaz Vue.
- docs: documentación y decisiones.

## 5. Modelo de recursos

Resource será la entidad central de la V1.

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

## 6. API

Los recursos expondrán inicialmente:

- GET /api/v1/resources
- GET /api/v1/resources/{id}
- POST /api/v1/resources
- PUT /api/v1/resources/{id}
- DELETE /api/v1/resources/{id}
- GET /api/v1/categories
- POST /api/v1/categories
- GET /api/v1/tags

La búsqueda se realizará mediante filtros de API. El frontend nunca accederá directamente a SQLite.

## 7. Seguridad

La autenticación utiliza sesiones server-side, cookies HttpOnly/Secure/SameSite y Argon2id. Las mutaciones requieren CSRF.

La acción administrativa de reinicio está limitada a una orden exacta de systemd mediante sudoers de mínimo privilegio. ControlHub no ejecuta comandos remotos arbitrarios.

Los secretos quedan fuera del modelo normal de recursos y se diseñará un subsistema cifrado separado.

## 8. Testing

Backend: pytest + Ruff. Frontend: Vitest + ESLint + build. Los flujos de navegador se cubrirán progresivamente con Playwright.

## 9. Internacionalización

El software empieza en castellano y la arquitectura evita acoplar de forma irreversible los textos a la lógica para permitir i18n futura.
