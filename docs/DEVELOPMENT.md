# Desarrollo

## Estado actual

ControlHub dispone de una primera base funcional con autenticación, sesiones server-side, panel inicial y una acción administrativa controlada para reiniciar el servicio.

## Producción en Debian

La arquitectura de producción es:

Apache HTTPS → Uvicorn/systemd → FastAPI → SQLite.

El backend escucha únicamente en loopback. El puerto interno se configura mediante `CONTROLHUB_PORT` y actualmente es 8008.

### Variables de entorno

Crear `/etc/controlhub/controlhub.env` fuera del repositorio. El archivo puede contener:

```text
CONTROLHUB_HOST=127.0.0.1
CONTROLHUB_PORT=8008
DATABASE_URL=sqlite:///data/controlhub.db
CONTROLHUB_ADMIN_USERNAME=<usuario>
CONTROLHUB_ADMIN_PASSWORD=<contraseña-inicial>
```

No almacenar secretos reales en Git.

### Servicio systemd

Crear `/etc/systemd/system/controlhub.service`:

```ini
[Unit]
Description=ControlHub FastAPI application
After=network.target

[Service]
Type=simple
User=stark
Group=stark
WorkingDirectory=/opt/controlhub/backend
EnvironmentFile=/etc/controlhub/controlhub.env
ExecStart=/opt/controlhub/backend/.venv/bin/uvicorn app.main:app --host ${CONTROLHUB_HOST} --port ${CONTROLHUB_PORT}
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Aplicar:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now controlhub.service
```

Comprobar:

```bash
sudo systemctl status controlhub.service
sudo journalctl -u controlhub.service -n 80 --no-pager
curl -i http://127.0.0.1:8008/api/v1/health
curl -i https://hub.warcrafted.com/api/v1/health
```

### Reinicio desde el panel

El panel no ejecuta comandos arbitrarios. La única orden que puede solicitar es:

```text
sudo -n /bin/systemctl restart controlhub.service
```

En el servidor se debe autorizar exclusivamente esa orden mediante `/etc/sudoers.d/controlhub`:

```text
stark ALL=(root) NOPASSWD: /bin/systemctl restart controlhub.service
```

Validar antes de probar el botón:

```bash
sudo visudo -cf /etc/sudoers.d/controlhub
sudo -u stark sudo -n /bin/systemctl restart controlhub.service
```

No autorizar `systemctl` genérico ni comandos adicionales.

### Despliegue

El botón de reinicio no actualiza el código. El flujo normal es:

1. Actualizar el código con Git.
2. Instalar dependencias si han cambiado.
3. Construir el frontend.
4. Ejecutar tests.
5. Ejecutar migraciones cuando existan.
6. Reiniciar `controlhub.service`.
7. Verificar `/api/v1/health`.

No se recomienda un file watcher para producción.

## Git

No se deben introducir contraseñas, API keys, tokens, claves privadas, certificados privados ni datos de producción en el repositorio.
