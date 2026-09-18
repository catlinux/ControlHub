<script setup lang="ts">
import { onMounted, ref } from "vue";

const authenticated = ref(false);
const username = ref("");
const loading = ref(true);
const message = ref("");
const error = ref("");

function csrfToken(): string {
  const match = document.cookie.match(/(?:^|; )controlhub_csrf=([^;]+)/);
  return match?.[1] ?? "";
}

async function loadSession() {
  const response = await fetch("/api/v1/auth/me", { cache: "no-store" });
  const data = await response.json();
  authenticated.value = data.authenticated;
  username.value = data.username ?? "";
  loading.value = false;
}

async function login(event: Event) {
  const form = event.target as HTMLFormElement;
  const formData = new FormData(form);
  const body = new URLSearchParams();
  const usernameField = formData.get("username");
  const passwordField = formData.get("password");

  if (typeof usernameField === "string") body.set("username", usernameField);
  if (typeof passwordField === "string") body.set("password", passwordField);

  const response = await fetch("/api/v1/auth/login", {
    method: "POST",
    body,
    redirect: "manual",
  });
  if (response.status !== 303) {
    error.value = "No se pudo iniciar sesión.";
    return;
  }

  await loadSession();
  if (!authenticated.value) error.value = "Credenciales no válidas.";
}

async function restart() {
  if (!confirm("¿Reiniciar ControlHub ahora? La aplicación estará unos segundos no disponible.")) {
    return;
  }

  message.value = "";
  error.value = "";

  const response = await fetch("/api/v1/admin/restart", {
    method: "POST",
    headers: { "X-CSRF-Token": csrfToken() },
  });

  if (!response.ok) {
    error.value = "No se pudo solicitar el reinicio.";
    return;
  }

  message.value = "Reinicio solicitado. Comprobando recuperación…";
  for (let i = 0; i < 15; i += 1) {
    await new Promise((resolve) => setTimeout(resolve, 1000));
    try {
      const health = await fetch("/api/v1/health", { cache: "no-store" });
      if (health.ok) {
        message.value = "ControlHub está de nuevo operativo.";
        return;
      }
    } catch (error) {
      console.debug("No se pudo consultar health durante el reinicio.", error);
    }
  }

  error.value = "No se ha podido verificar la recuperación.";
}

async function logout() {
  await fetch("/api/v1/auth/logout", {
    method: "POST",
    headers: { "X-CSRF-Token": csrfToken() },
  });
  await loadSession();
}

onMounted(loadSession);
</script>

<template>
  <main class="app">
    <section class="panel">
      <p class="eyebrow">ControlHub</p>
      <template v-if="loading"><h1>Cargando…</h1></template>
      <template v-else-if="!authenticated">
        <h1>Centro de control</h1>
        <p>Inicia sesión para acceder al panel.</p>
        <form class="form" @submit.prevent="login">
          <label>Usuario<input name="username" autocomplete="username" required /></label>
          <label>Contraseña<input name="password" type="password" autocomplete="current-password" required /></label>
          <button type="submit">Iniciar sesión</button>
        </form>
        <p v-if="error" class="error">{{ error }}</p>
      </template>
      <template v-else>
        <h1>Centro de control</h1>
        <p>Sesión activa: <strong>{{ username }}</strong></p>
        <div class="actions">
          <button type="button" @click="restart">Reiniciar ControlHub</button>
          <button type="button" class="secondary" @click="logout">Cerrar sesión</button>
        </div>
        <p v-if="message" class="message">{{ message }}</p>
        <p v-if="error" class="error">{{ error }}</p>
      </template>
    </section>
  </main>
</template>
