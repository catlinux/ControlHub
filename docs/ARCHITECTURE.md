# Arquitectura

## 1. Objetivo

La arquitectura de ControlHub debe proporcionar una base sencilla para la primera versión y, al mismo tiempo, permitir la incorporación progresiva de nuevos tipos de recursos, integraciones y funciones de supervisión.

## 2. Enfoque

La V1 seguirá inicialmente un enfoque de **monolito modular**, evitando microservicios y complejidad distribuida mientras no exista una necesidad real que los justifique.

La separación lógica deberá permitir evolucionar posteriormente componentes concretos sin tener que rediseñar toda la aplicación.

## 11. Capas conceptuales

```text
┌─────────────────────────────┐
│          Frontend           │
├─────────────────────────────┤
│             API             │
├─────────────────────────────┤
│       Lógica de negocio     │
├─────────────────────────────┤
│ Persistencia / Base de datos│
└─────────────────────────────┘

        Integraciones externas
                 │
                 ▼
        ┌─────────────────┐
        │  Integrations   │
        └─────────────────┘
```

## 3. Stack tecnológico

- Backend: Python + FastAPI + SQLModel + Alembic + Uvicorn
- Frontend: Vue 3 + TypeScript + Tailwind CSS + Pinia + Vue I18n
- Base de datos V1: SQLite
- API REST versionada bajo `/api/v1`
- Autenticación mediante sesiones server-side y cookies seguras
- Contraseñas con Argon2id
- Producción: Apache HTTPS → Uvicorn/systemd → FastAPI → SQLite
- V1 sin Docker

## 4. Estructura del repositorio

Monorepo con frontend, backend, documentación, tests y scripts. La implementación funcional todavía no ha comenzado.

## 5. API y seguridad

El frontend nunca accede directamente a SQLite. FastAPI escuchará únicamente en loopback en producción. La API aplicará validación de entrada, CORS restringido, CSRF, límites de petición, rate limiting en endpoints sensibles y respuestas de error coherentes.

## 6. Autenticación y autorización

Se utilizarán sesiones server-side, cookies HttpOnly/Secure/SameSite y el modelo `User → Role → Permission`. La V1 tendrá inicialmente un rol administrativo, sin hardcodear la autorización.

## 7. Panel de administración

La administración forma parte de la V1 e incluirá recursos, categorías, tags, usuarios, roles/permisos, secretos, auditoría y configuración. Gestionar un recurso no implica ejecutar el servicio asociado.

## 8. Auditoría y logs

Se separarán los logs operativos de la auditoría. Ninguno almacenará contraseñas, tokens, claves privadas ni contenido de secretos.

## 9. Testing y CI

Backend con pytest; frontend con Vitest; flujos críticos con Playwright. GitHub Actions ejecutará lint, tests, build y comprobaciones de calidad.

## 10. Evolución

La arquitectura queda preparada para PostgreSQL, monitorización, integraciones externas y acciones remotas controladas cuando exista una necesidad real.

## 4. Recurso como entidad central

El concepto principal de ControlHub será `Resource`.

Un recurso podrá representar diferentes clases de elementos digitales sin obligar a crear un modelo completamente independiente para cada tipo.

Conceptualmente:

```text
Resource
├── identity
│   ├── name
│   ├── description
│   └── type
├── organization
│   ├── category
│   ├── tags
│   └── favorite
├── connection
│   ├── url
│   ├── host
│   ├── port
│   └── username
├── presentation
│   ├── icon
│   └── status
└── metadata
    └── type-specific data
```

## 5. Secretos

Las credenciales y secretos no deben almacenarse como texto plano dentro del modelo normal de recursos.

El modelo de recursos podrá contener referencias o información no sensible necesaria para identificar o conectar con un recurso, mientras que contraseñas, tokens, claves privadas y otros secretos deberán gestionarse mediante un mecanismo separado.

La solución concreta de almacenamiento de secretos se definirá durante el diseño de seguridad.

## 6. Seguridad

La seguridad es un requisito arquitectónico desde la V1.

Se deberán considerar como mínimo:

- autenticación;
- autorización;
- gestión segura de sesiones;
- protección frente a CSRF y XSS cuando corresponda;
- validación de entradas;
- gestión de secretos;
- HTTPS en producción;
- control de acceso;
- logs;
- mínimo privilegio.

ControlHub no deberá ejecutar comandos remotos arbitrarios simplemente como consecuencia de una acción de interfaz.

## 7. Internacionalización

La aplicación comenzará en castellano, pero la arquitectura deberá evitar que los textos estén acoplados de forma irreversible al código.

La internacionalización se preparará desde el principio para permitir incorporar otros idiomas posteriormente.
