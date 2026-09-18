# Desarrollo

## Estado actual

ControlHub dispone de autenticación, sesiones server-side, panel responsive, recursos, categorías, tags, administración básica, auditoría y almacenamiento cifrado de secretos separado del modelo Resource.

## Producción en Debian

Arquitectura:

Apache HTTPS -> Uvicorn/systemd -> FastAPI -> SQLite.

El backend escucha únicamente en loopback y usa el puerto interno 8008.

### Configuración

La configuración de producción se mantiene fuera del repositorio:

/etc/controlhub/controlhub.env

Debe contener como mínimo:

CONTROLHUB_HOST=127.0.0.1
CONTROLHUB_PORT=8008
DATABASE_URL=sqlite:///data/controlhub.db
CONTROLHUB_ADMIN_USERNAME=<usuario>
CONTROLHUB_ADMIN_PASSWORD=<contraseña-inicial>
CONTROLHUB_SECRET_KEY=<clave-Fernet-generada-fuera-del-repositorio>

La clave Fernet debe mantenerse fuera de Git y fuera de la base de datos. No debe compartirse en incidencias, logs ni documentación pública.

### Base de datos

Alembic es el mecanismo único de evolución del esquema.

La aplicación ejecuta las migraciones al iniciar. Si encuentra una base existente sin tabla alembic_version, la marca como compatible con la migración inicial y aplica las migraciones posteriores.

Para nuevas instalaciones también puede ejecutarse explícitamente:

cd backend
.venv/bin/alembic upgrade head

### Servicio

sudo systemctl daemon-reload
sudo systemctl enable --now controlhub.service
sudo systemctl status controlhub.service

Verificación:

curl -fsS http://127.0.0.1:8008/api/v1/health
curl -fsS https://hub.warcrafted.com/api/v1/health

### Reinicio administrativo

El panel sólo puede solicitar:

sudo -n /bin/systemctl restart controlhub.service

Sudoers:

stark ALL=(root) NOPASSWD: /bin/systemctl restart controlhub.service

No se debe autorizar systemctl genérico ni comandos adicionales.

## Desarrollo local

Backend:

cd backend
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/ruff check .
.venv/bin/pytest -q

Frontend:

cd frontend
npm install
npm run lint
npm run test
npm run build

El lockfile generado localmente no se versiona actualmente.

## Secretos

Los valores secretos se cifran con Fernet. Resource no almacena secretos.

La API de secretos sólo devuelve metadatos; nunca devuelve el valor ni el ciphertext. Las operaciones de escritura requieren sesión administrativa y CSRF.

## Despliegue

1. Actualizar el código con Git.
2. Instalar dependencias si han cambiado.
3. Ejecutar Ruff y pytest.
4. Ejecutar lint, tests y build del frontend.
5. Verificar migraciones Alembic.
6. Configurar secretos fuera del repositorio.
7. Reiniciar controlhub.service.
8. Verificar health local y HTTPS.
9. Verificar login y flujos administrativos.
10. Revisar Git y documentación.

No se utiliza file watcher en producción.
