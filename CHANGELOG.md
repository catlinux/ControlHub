# Changelog

Todos los cambios relevantes de ControlHub se documentarán en este archivo.

## [Unreleased]

### Añadido

- Primera base funcional de autenticación con sesiones server-side.
- Rol administrativo inicial.
- Panel web responsive.
- Protección CSRF para las acciones de sesión y administración.
- Auditoría mínima de login, logout y acciones administrativas.
- Persistencia mediante SQLModel.
- Entidades Category, Tag, Resource y Secret.
- CRUD inicial de recursos.
- Búsqueda y filtros.
- URLs, host, puerto, usuario y copia de comandos SSH.
- Gestión administrativa básica de usuarios, roles y contraseñas.
- Almacén de secretos cifrados separado de Resource.
- Rate limiting básico para login y operaciones administrativas sensibles.
- Alembic como mecanismo único de migraciones.
- Portal principal privado orientado a accesos directos.
- Resumen visual de recursos, estados, favoritos y categorías.
- Agrupación de recursos por categoría.
- Administración modal separada del portal.
- Secciones administrativas para usuarios, secretos, auditoría y sistema.
- Protección explícita contra indexación mediante meta robots, X-Robots-Tag y robots.txt.

### Cambiado

- La persistencia de autenticación utiliza SQLModel.
- La pantalla principal pasa de un dashboard administrativo a un portal de accesos directos.
- Los recursos se presentan agrupados visualmente por categoría.
- La administración deja de ocupar la pantalla principal y se abre como modal por secciones.
- Los usuarios no administradores utilizan ControlHub como portal y no reciben controles de gestión de recursos o categorías.
- La gestión de recursos y categorías queda restringida al rol administrador.
- La acción de reinicio pasa al área administrativa.
- La configuración de producción se mantiene fuera del repositorio en /etc/controlhub/controlhub.env.
- La inicialización de base de datos utiliza Alembic.

### Corregido

- Artefactos __pycache__ quedan excluidos del repositorio.
- Carga de los modelos SQLModel al iniciar FastAPI.
- Inicio de sesión con objetos User de SQLModel.
- Pruebas de cookies Secure mediante TestClient sobre HTTPS.
- Textos restantes del dashboard que no estaban en castellano.

### Pendiente

- Pruebas de navegador y E2E.
- Estados técnicos activos de recursos.
- Revisión final de accesibilidad y contratos OpenAPI.
- Configuración de CONTROLHUB_SECRET_KEY en producción antes de utilizar secretos.
