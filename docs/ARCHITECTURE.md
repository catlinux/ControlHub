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

Los detalles concretos del framework, lenguaje y motor de base de datos se decidirán antes de comenzar la implementación.

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
