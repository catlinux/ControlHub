<script setup lang="ts">
import { onMounted, ref } from "vue";

type Resource = {
  id: number;
  name: string;
  description: string;
  category_id: number | null;
  resource_type: string;
  url: string;
  host: string;
  port: number | null;
  username: string;
  icon: string;
  status: string;
  favorite: boolean;
  notes: string;
  tags: string[];
};

type Category = { id: number; name: string };

const authenticated = ref(false);
const username = ref("");
const loading = ref(true);
const resources = ref<Resource[]>([]);
const categories = ref<Category[]>([]);
const search = ref("");
const favoriteOnly = ref(false);
const categoryFilter = ref("");
const message = ref("");
const error = ref("");
const showForm = ref(false);
const editingId = ref<number | null>(null);

const form = ref({
  name: "",
  description: "",
  category_id: null as number | null,
  resource_type: "web",
  url: "",
  host: "",
  port: null as number | null,
  username: "",
  icon: "",
  status: "unknown",
  favorite: false,
  notes: "",
  tags: "",
});

function csrfToken() {
  const match = document.cookie.match(/(?:^|; )controlhub_csrf=([^;]+)/);
  return match?.[1] ?? "";
}

function resetForm() {
  editingId.value = null;
  form.value = {
    name: "",
    description: "",
    category_id: null,
    resource_type: "web",
    url: "",
    host: "",
    port: null,
    username: "",
    icon: "",
    status: "unknown",
    favorite: false,
    notes: "",
    tags: "",
  };
}

async function loadData() {
  const params = new URLSearchParams();
  if (search.value.trim()) params.set("search", search.value.trim());
  if (categoryFilter.value) params.set("category_id", categoryFilter.value);
  if (favoriteOnly.value) params.set("favorite", "true");

  const [resourcesResponse, categoriesResponse] = await Promise.all([
    fetch("/api/v1/resources?" + params.toString(), { cache: "no-store" }),
    fetch("/api/v1/categories", { cache: "no-store" }),
  ]);

  if (!resourcesResponse.ok || !categoriesResponse.ok) {
    throw new Error("No se pudieron cargar los recursos.");
  }

  resources.value = await resourcesResponse.json();
  categories.value = await categoriesResponse.json();
}

async function loadSession() {
  const response = await fetch("/api/v1/auth/me", { cache: "no-store" });
  const data = await response.json();
  authenticated.value = data.authenticated;
  username.value = data.username ?? "";
  loading.value = false;
  if (authenticated.value) {
    try {
      await loadData();
    } catch (loadError) {
      error.value = loadError instanceof Error ? loadError.message : "Error de carga.";
    }
  }
}

function openCreate() {
  resetForm();
  showForm.value = true;
}

function openEdit(resource: Resource) {
  editingId.value = resource.id;
  form.value = {
    name: resource.name,
    description: resource.description,
    category_id: resource.category_id,
    resource_type: resource.resource_type,
    url: resource.url,
    host: resource.host,
    port: resource.port,
    username: resource.username,
    icon: resource.icon,
    status: resource.status,
    favorite: resource.favorite,
    notes: resource.notes,
    tags: resource.tags.join(", "),
  };
  showForm.value = true;
}

async function login(event: Event) {
  const element = event.target as HTMLFormElement;
  const data = new FormData(element);
  const body = new URLSearchParams();
  body.set("username", String(data.get("username") ?? ""));
  body.set("password", String(data.get("password") ?? ""));

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
}

async function saveResource() {
  error.value = "";
  const payload = {
    ...form.value,
    tags: form.value.tags.split(",").map((item) => item.trim()).filter(Boolean),
    metadata: {},
  };
  const url = editingId.value
    ? "/api/v1/resources/" + editingId.value
    : "/api/v1/resources";

  const response = await fetch(url, {
    method: editingId.value ? "PUT" : "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRF-Token": csrfToken(),
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    error.value = "No se pudo guardar el recurso.";
    return;
  }

  showForm.value = false;
  message.value = editingId.value ? "Recurso actualizado." : "Recurso creado.";
  resetForm();
  await loadData();
}

async function removeResource(resource: Resource) {
  if (!confirm("¿Eliminar «" + resource.name + "»?")) return;
  const response = await fetch("/api/v1/resources/" + resource.id, {
    method: "DELETE",
    headers: { "X-CSRF-Token": csrfToken() },
  });
  if (!response.ok) {
    error.value = "No se pudo eliminar el recurso.";
    return;
  }
  message.value = "Recurso eliminado.";
  await loadData();
}

async function copySsh(resource: Resource) {
  const port = resource.port ? " -p " + resource.port : "";
  const user = resource.username || "usuario";
  await navigator.clipboard.writeText("ssh" + port + " " + user + "@" + resource.host);
  message.value = "Comando SSH copiado.";
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

async function logout() {
  await fetch("/api/v1/auth/logout", {
    method: "POST",
    headers: { "X-CSRF-Token": csrfToken() },
  });
  authenticated.value = false;
  resources.value = [];
}

onMounted(loadSession);
</script>

<template>
  <main class="app">
    <section class="panel">
      <header class="topbar">
        <div>
          <p class="eyebrow">ControlHub</p>
          <h1>Centro de control</h1>
        </div>
        <div v-if="authenticated" class="session">
          <span>{{ username }}</span>
          <button class="secondary" type="button" @click="logout">Salir</button>
        </div>
      </header>

      <template v-if="loading">
        <p>Cargando…</p>
      </template>

      <template v-else-if="!authenticated">
        <p>Inicia sesión para acceder al panel.</p>
        <form class="form narrow" @submit.prevent="login">
          <label>Usuario<input name="username" autocomplete="username" required /></label>
          <label>Contraseña<input name="password" type="password" autocomplete="current-password" required /></label>
          <button type="submit">Iniciar sesión</button>
        </form>
      </template>

      <template v-else>
        <div class="toolbar">
          <input v-model="search" type="search" placeholder="Buscar recursos…" @input="loadData" />
          <select v-model="categoryFilter" @change="loadData">
            <option value="">Todas las categorías</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
          <label class="check"><input v-model="favoriteOnly" type="checkbox" @change="loadData" /> Favoritos</label>
          <button type="button" @click="openCreate">+ Recurso</button>
          <button class="secondary" type="button" @click="restart">Reiniciar</button>
        </div>

        <div v-if="resources.length" class="resource-grid">
          <article v-for="resource in resources" :key="resource.id" class="resource-card">
            <div class="card-head">
              <div>
                <span class="type">{{ resource.resource_type }}</span>
                <h2>{{ resource.icon ? resource.icon + " " : "" }}{{ resource.name }}</h2>
              </div>
              <span :class="['status', resource.status]">{{ resource.status }}</span>
            </div>
            <p v-if="resource.description">{{ resource.description }}</p>
            <p v-if="resource.host" class="connection">
              {{ resource.username ? resource.username + "@" : "" }}{{ resource.host }}{{ resource.port ? ":" + resource.port : "" }}
            </p>
            <div class="tags">
              <span v-for="tag in resource.tags" :key="tag">{{ tag }}</span>
            </div>
            <div class="card-actions">
              <a v-if="resource.url" :href="resource.url" target="_blank" rel="noreferrer">Obrir</a>
              <button v-if="resource.host" type="button" @click="copySsh(resource)">Copiar SSH</button>
              <button type="button" @click="openEdit(resource)">Editar</button>
              <button class="danger" type="button" @click="removeResource(resource)">Eliminar</button>
            </div>
          </article>
        </div>

        <div v-else class="empty">
          <h2>Encara no hi ha recursos</h2>
          <p>Afegeix el primer recurs per començar.</p>
          <button type="button" @click="openCreate">Crear recurs</button>
        </div>

        <p v-if="message" class="message">{{ message }}</p>
        <p v-if="error" class="error">{{ error }}</p>
      </template>
    </section>

    <div v-if="showForm" class="modal-backdrop" @click.self="showForm = false">
      <section class="modal">
        <header class="modal-head">
          <h2>{{ editingId ? "Editar recurso" : "Nuevo recurso" }}</h2>
          <button class="secondary" type="button" @click="showForm = false">×</button>
        </header>
        <form class="form" @submit.prevent="saveResource">
          <label>Nombre<input v-model="form.name" required maxlength="200" /></label>
          <label>Descripción<textarea v-model="form.description" rows="2" /></label>
          <div class="form-grid">
            <label>Tipo
              <select v-model="form.resource_type">
                <option value="web">Web</option>
                <option value="server">Servidor</option>
                <option value="ssh">SSH</option>
                <option value="service">Servicio</option>
                <option value="database">Base de datos</option>
                <option value="git">Git</option>
                <option value="cloud">Cloud</option>
                <option value="other">Otro</option>
              </select>
            </label>
            <label>Categoría
              <select v-model="form.category_id">
                <option :value="null">Sin categoría</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
              </select>
            </label>
          </div>
          <label>URL<input v-model="form.url" type="url" placeholder="https://…" /></label>
          <div class="form-grid">
            <label>Host/IP<input v-model="form.host" /></label>
            <label>Puerto<input v-model.number="form.port" type="number" min="1" max="65535" /></label>
          </div>
          <div class="form-grid">
            <label>Usuario<input v-model="form.username" /></label>
            <label>Icono<input v-model="form.icon" placeholder="🖥️" /></label>
          </div>
          <label>Tags<input v-model="form.tags" placeholder="producción, linux, web" /></label>
          <label>Notas<textarea v-model="form.notes" rows="3" /></label>
          <label class="check"><input v-model="form.favorite" type="checkbox" /> Favorito</label>
          <div class="modal-actions">
            <button class="secondary" type="button" @click="showForm = false">Cancelar</button>
            <button type="submit">Guardar</button>
          </div>
        </form>
      </section>
    </div>
  </main>
</template>
