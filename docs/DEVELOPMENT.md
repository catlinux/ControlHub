# Desarrollo

## Estado actual

ControlHub dispone de autenticación, sesiones server-side, panel responsive y reinicio administrativo. La siguiente etapa implementará el CRUD de recursos de la V1.

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

Los secretos reales nunca se introducen en Git.

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
.venv/bin/pytest -q

Frontend:

cd frontend
npm install
npm run lint
npm run test
npm run build

El lockfile generado localmente no se versiona actualmente; la política de lockfiles deberá decidirse explícitamente.

## Despliegue

1. Actualizar el código con Git.
2. Instalar dependencias si han cambiado.
3. Ejecutar tests.
4. Construir frontend.
5. Ejecutar migraciones cuando corresponda.
6. Reiniciar controlhub.service.
7. Verificar health y flujos críticos.

No se utiliza file watcher en producción.
