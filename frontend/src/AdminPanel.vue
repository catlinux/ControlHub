<script setup lang="ts">
import { onMounted, ref } from "vue";

type User = { id: number; username: string; role: string; created_at: string };
type Secret = { id: number; name: string; description: string };
type AuditRow = { id: number; user_id: number | null; action: string; created_at: string };

const users = ref<User[]>([]);
const secrets = ref<Secret[]>([]);
const auditRows = ref<AuditRow[]>([]);
const message = ref("");
const error = ref("");
const newUser = ref({ username: "", password: "", role: "user" });
const newSecret = ref({ name: "", description: "", value: "" });

function csrfToken() {
  const match = document.cookie.match(/(?:^|; )controlhub_csrf=([^;]+)/);
  return match?.[1] ?? "";
}

async function load() {
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

onMounted(async () => {
  try {
    await load();
  } catch (loadError) {
    error.value = loadError instanceof Error ? loadError.message : "Error de carga.";
  }
});
</script>

<template>
  <section class="admin-panel">
    <header>
      <p class="eyebrow">Administración</p>
      <h2>Usuarios, secretos y auditoría</h2>
    </header>
    <div class="admin-grid">
      <article class="admin-card">
        <h3>Usuarios</h3>
        <form class="form" @submit.prevent="createUser">
          <input v-model="newUser.username" placeholder="Usuario" required />
          <input v-model="newUser.password" type="password" minlength="12" placeholder="Contraseña (12+)" required />
          <select v-model="newUser.role">
            <option value="user">Usuario</option>
            <option value="admin">Administrador</option>
          </select>
          <button type="submit">Crear usuario</button>
        </form>
        <ul class="admin-list">
          <li v-for="user in users" :key="user.id">
            <span>{{ user.username }} · {{ user.role }}</span>
            <span>
              <button class="secondary" type="button" @click="changeRole(user)">Cambiar rol</button>
              <button class="danger" type="button" @click="removeUser(user)">Eliminar</button>
            </span>
          </li>
        </ul>
      </article>
      <article class="admin-card">
        <h3>Secretos cifrados</h3>
        <p class="hint">El valor nunca se muestra después de guardarlo.</p>
        <form class="form" @submit.prevent="createSecret">
          <input v-model="newSecret.name" placeholder="Nombre" required />
          <input v-model="newSecret.description" placeholder="Descripción" />
          <input v-model="newSecret.value" type="password" placeholder="Valor secreto" required />
          <button type="submit">Guardar secreto</button>
        </form>
        <ul class="admin-list">
          <li v-for="secret in secrets" :key="secret.id">
            <span>{{ secret.name }}<small v-if="secret.description"> · {{ secret.description }}</small></span>
            <button class="danger" type="button" @click="removeSecret(secret)">Eliminar</button>
          </li>
        </ul>
      </article>
      <article class="admin-card">
        <h3>Auditoría reciente</h3>
        <ul class="audit-list">
          <li v-for="row in auditRows" :key="row.id">
            <span>{{ row.action }}</span>
            <small>{{ row.created_at }}</small>
          </li>
        </ul>
      </article>
    </div>
    <p v-if="message" class="message">{{ message }}</p>
    <p v-if="error" class="error">{{ error }}</p>
  </section>
</template>
