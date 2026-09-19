<script setup lang="ts">
import { onMounted, ref } from "vue";

type User = { id: number; username: string; role: string; created_at: string };
type Secret = { id: number; name: string; description: string };
type AuditRow = { id: number; user_id: number | null; action: string; created_at: string };

const emit = defineEmits<{ close: [] }>();

const activeTab = ref<"users" | "secrets" | "audit" | "system">("users");
const users = ref<User[]>([]);
const secrets = ref<Secret[]>([]);
const auditRows = ref<AuditRow[]>([]);
const message = ref("");
const error = ref("");
const loading = ref(true);
const newUser = ref({ username: "", password: "", role: "user" });
const newSecret = ref({ name: "", description: "", value: "" });

function csrfToken() {
  const match = document.cookie.match(/(?:^|; )controlhub_csrf=([^;]+)/);
  return match?.[1] ?? "";
}

async function load() {
  loading.value = true;
  try {
    const [usersResponse, secretsResponse, auditResponse] = await Promise.all([
      fetch("/api/v1/admin/users", { cache: "no-store" }),
      fetch("/api/v1/secrets", { cache: "no-store" }),
      fetch("/api/v1/admin/audit", { cache: "no-store" }),
    ]);

    if (!usersResponse.ok || !secretsResponse.ok || !auditResponse.ok) {
      throw new Error("No se pudo cargar la administración.");
    }

    users.value = await usersResponse.json();
    secrets.value = await secretsResponse.json();
    auditRows.value = await auditResponse.json();
  } catch (loadError) {
    error.value = loadError instanceof Error ? loadError.message : "Error de carga.";
  } finally {
    loading.value = false;
  }
}

async function createUser() {
  const response = await fetch("/api/v1/admin/users", {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRF-Token": csrfToken() },
    body: JSON.stringify(newUser.value),
  });

  if (!response.ok) {
    error.value = "No se pudo crear el usuario.";
    return;
  }

  newUser.value = { username: "", password: "", role: "user" };
  message.value = "Usuario creado.";
  await load();
}

async function changeRole(user: User) {
  const role = user.role === "admin" ? "user" : "admin";
  const response = await fetch("/api/v1/admin/users/" + user.id + "/role", {
    method: "PATCH",
    headers: { "Content-Type": "application/json", "X-CSRF-Token": csrfToken() },
    body: JSON.stringify({ role }),
  });

  if (!response.ok) {
    error.value = "No se pudo cambiar el rol.";
    return;
  }

  message.value = "Rol actualizado.";
  await load();
}

async function removeUser(user: User) {
  if (!confirm("¿Eliminar el usuario «" + user.username + "»?")) return;

  const response = await fetch("/api/v1/admin/users/" + user.id, {
    method: "DELETE",
    headers: { "X-CSRF-Token": csrfToken() },
  });

  if (!response.ok) {
    error.value = "No se pudo eliminar el usuario.";
    return;
  }

  message.value = "Usuario eliminado.";
  await load();
}

async function createSecret() {
  const response = await fetch("/api/v1/secrets", {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRF-Token": csrfToken() },
    body: JSON.stringify(newSecret.value),
  });

  if (!response.ok) {
    error.value = response.status === 503
      ? "La clave de cifrado no está configurada en el servidor."
      : "No se pudo guardar el secreto.";
    return;
  }

  newSecret.value = { name: "", description: "", value: "" };
  message.value = "Secreto cifrado y guardado.";
  await load();
}

async function removeSecret(secret: Secret) {
  if (!confirm("¿Eliminar el secreto «" + secret.name + "»?")) return;

  const response = await fetch("/api/v1/secrets/" + secret.id, {
    method: "DELETE",
    headers: { "X-CSRF-Token": csrfToken() },
  });

  if (!response.ok) {
    error.value = "No se pudo eliminar el secreto.";
    return;
  }

  message.value = "Secreto eliminado.";
  await load();
}

async function restart() {
  if (!confirm("¿Reiniciar ControlHub ahora?")) return;

  const response = await fetch("/api/v1/admin/restart", {
    method: "POST",
    headers: { "X-CSRF-Token": csrfToken() },
  });

  if (!response.ok) {
    error.value = "No se pudo solicitar el reinicio.";
    return;
  }

  message.value = "Reinicio solicitado. Esperando recuperación…";
  for (let index = 0; index < 15; index += 1) {
    await new Promise((resolve) => setTimeout(resolve, 1000));
    try {
      const health = await fetch("/api/v1/health", { cache: "no-store" });
      if (health.ok) {
        message.value = "ControlHub está operativo.";
        return;
      }
    } catch (restartError) {
      console.debug("Health no disponible durante el reinicio.", restartError);
    }
  }

  error.value = "No se pudo verificar la recuperación.";
}

onMounted(load);
</script>

<template>
  <div class="modal-backdrop admin-backdrop" @click.self="emit('close')">
    <section class="modal admin-modal" role="dialog" aria-modal="true" aria-labelledby="admin-title">
      <header class="modal-head">
        <div>
          <p class="eyebrow">ControlHub</p>
          <h2 id="admin-title">Administración</h2>
        </div>
        <button class="icon-button" type="button" aria-label="Cerrar administración" @click="emit('close')">×</button>
      </header>

      <nav class="admin-tabs" aria-label="Secciones de administración">
        <button :class="{ active: activeTab === 'users' }" type="button" @click="activeTab = 'users'">
          Usuarios <span>{{ users.length }}</span>
        </button>
        <button :class="{ active: activeTab === 'secrets' }" type="button" @click="activeTab = 'secrets'">
          Secretos <span>{{ secrets.length }}</span>
        </button>
        <button :class="{ active: activeTab === 'audit' }" type="button" @click="activeTab = 'audit'">
          Auditoría <span>{{ auditRows.length }}</span>
        </button>
        <button :class="{ active: activeTab === 'system' }" type="button" @click="activeTab = 'system'">
          Sistema
        </button>
      </nav>

      <div v-if="loading" class="admin-loading">Cargando administración…</div>

      <div v-else class="admin-content">
        <section v-if="activeTab === 'users'">
          <div class="admin-section-heading">
            <div>
              <h3>Usuarios</h3>
              <p>Gestiona las cuentas y sus permisos.</p>
            </div>
          </div>
          <form class="form admin-form" @submit.prevent="createUser">
            <div class="form-grid">
              <label>Usuario<input v-model="newUser.username" autocomplete="off" required /></label>
              <label>Contraseña<input v-model="newUser.password" type="password" minlength="12" required /></label>
            </div>
            <div class="admin-form-row">
              <select v-model="newUser.role" aria-label="Rol del nuevo usuario">
                <option value="user">Usuario</option>
                <option value="admin">Administrador</option>
              </select>
              <button type="submit">Crear usuario</button>
            </div>
          </form>
          <ul class="admin-list">
            <li v-for="user in users" :key="user.id">
              <div>
                <strong>{{ user.username }}</strong>
                <small>{{ user.role === "admin" ? "Administrador" : "Usuario" }}</small>
              </div>
              <div class="inline-actions">
                <button class="secondary" type="button" @click="changeRole(user)">Cambiar rol</button>
                <button class="danger" type="button" @click="removeUser(user)">Eliminar</button>
              </div>
            </li>
          </ul>
        </section>

        <section v-else-if="activeTab === 'secrets'">
          <div class="admin-section-heading">
            <div>
              <h3>Secretos cifrados</h3>
              <p>Los valores se almacenan cifrados y nunca se muestran después de guardarlos.</p>
            </div>
          </div>
          <form class="form admin-form" @submit.prevent="createSecret">
            <label>Nombre<input v-model="newSecret.name" required /></label>
            <label>Descripción<input v-model="newSecret.description" /></label>
            <label>Valor secreto<input v-model="newSecret.value" type="password" autocomplete="new-password" required /></label>
            <div class="admin-form-row">
              <span></span>
              <button type="submit">Guardar secreto</button>
            </div>
          </form>
          <ul class="admin-list">
            <li v-for="secret in secrets" :key="secret.id">
              <div>
                <strong>{{ secret.name }}</strong>
                <small v-if="secret.description">{{ secret.description }}</small>
              </div>
              <button class="danger" type="button" @click="removeSecret(secret)">Eliminar</button>
            </li>
          </ul>
        </section>

        <section v-else-if="activeTab === 'audit'">
          <div class="admin-section-heading">
            <div>
              <h3>Auditoría reciente</h3>
              <p>Actividad administrativa registrada por ControlHub.</p>
            </div>
            <span class="result-count">{{ auditRows.length }} eventos</span>
          </div>
          <div class="audit-list-container">
            <ul class="audit-list">
              <li v-for="row in auditRows" :key="row.id">
                <div>
                  <strong>{{ row.action }}</strong>
                  <small>Usuario #{{ row.user_id ?? "sistema" }}</small>
                </div>
                <time>{{ row.created_at }}</time>
              </li>
            </ul>
          </div>
        </section>

        <section v-else>
          <div class="admin-section-heading">
            <div>
              <h3>Sistema</h3>
              <p>Acciones operativas limitadas y controladas.</p>
            </div>
          </div>
          <div class="system-card">
            <div>
              <strong>Reiniciar ControlHub</strong>
              <p>Reinicia únicamente el servicio de ControlHub mediante la acción autorizada del sistema.</p>
            </div>
            <button class="danger" type="button" @click="restart">Reiniciar servicio</button>
          </div>
        </section>
      </div>

      <p v-if="message" class="message">{{ message }}</p>
      <p v-if="error" class="error">{{ error }}</p>
    </section>
  </div>
</template>
