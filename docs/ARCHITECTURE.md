# Arquitectura

## 1. Objetivo

La arquitectura de ControlHub debe proporcionar una base sencilla para la primera versión y, al mismo tiempo, permitir la incorporación progresiva de nuevos tipos de recursos, integraciones y funciones de supervisión.

## 2. Enfoque

La V1 seguirá inicialmente un enfoque de **monolito modular**, evitando microservicios y complejidad distribuida mientras no exista una necesidad real que los justifique.

La separación lógica deberá permitir evolucionar posteriormente componentes concretos sin tener que rediseñar toda la aplicación.

## 3. Capas conceptuales

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

## 4. Stack tecnológico

- Backend: Python + FastAPI + SQLModel + Alembic + Uvicorn
- Frontend: Vue 3 + TypeScript + Tailwind CSS + Pinia + Vue I18n
- Base de datos V1: SQLite
- API REST versionada bajo `/api/v1`
- Autenticación mediante sesiones server-side y cookies seguras
- Contraseñas con Argon2id
- Producción: Apache HTTPS → Uvicorn/systemd → FastAPI → SQLite
- V1 sin Docker

## 5. Estructura del repositorio

Monorepo con frontend, backend, documentación, tests y scripts.

La aplicación se implementará como un monolito modular. Las responsabilidades de API, autenticación, lógica de negocio y persistencia deben permanecer separadas aunque se ejecuten como un único servicio.

## 6. API y seguridad

El frontend nunca accede directamente a SQLite. FastAPI escucha únicamente en loopback en producción. La API debe aplicar validación de entrada, CORS restringido, CSRF, límites de petición, rate limiting en endpoints sensibles y respuestas de error coherentes.

## 7. Autenticación y autorización

Se utilizan sesiones server-side, cookies HttpOnly/Secure/SameSite y el modelo `User → Role → Permission`. La V1 comienza con un rol administrativo.

La implementación inicial de autenticación del prototipo utiliza SQLite mediante el módulo estándar `sqlite3` para poder validar el flujo completo rápidamente. Esto es una implementación transitoria: antes de ampliar el modelo funcional de V1, las tablas de autenticación deberán integrarse en el modelo SQLModel y gestionarse mediante Alembic, manteniendo una única estrategia de persistencia.

## 8. Panel de administración

La administración forma parte de la V1 e incluirá recursos, categorías, tags, usuarios, roles/permisos, secretos, auditoría y configuración.

La acción actual de reinicio está limitada a `controlhub.service`. No se permite ejecutar comandos arbitrarios desde la interfaz.

## 9. Auditoría y logs

Se separarán los logs operativos de la auditoría. Ninguno almacenará contraseñas, tokens, claves privadas ni contenido de secretos.

## 10. Testing y CI

Backend con pytest y Ruff; frontend con Vitest, ESLint y build de producción. Los flujos críticos se cubrirán progresivamente con Playwright. GitHub Actions ejecutará las comprobaciones del backend y frontend.

## 11. Recurso como entidad central

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

## 12. Secretos

Las credenciales y secretos no deben almacenarse como texto plano dentro del modelo normal de recursos.

El modelo de recursos podrá contener referencias o información no sensible necesaria para identificar o conectar con un recurso, mientras que contraseñas, tokens, claves privadas y otros secretos deberán gestionarse mediante un mecanismo separado.

La solución concreta de almacenamiento de secretos se definirá durante el diseño de seguridad.

## 13. Seguridad

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

## 14. Internacionalización

La aplicación comenzará en castellano, pero la arquitectura deberá evitar que los textos estén acoplados de forma irreversible al código.

La internacionalización se preparará desde el principio para permitir incorporar otros idiomas posteriormente.
