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
