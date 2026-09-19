<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import AdminPanel from "./AdminPanel.vue";

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
type Tag = { id: number; name: string };

const authenticated = ref(false);
const username = ref("");
const role = ref("");
const loading = ref(true);
const resources = ref<Resource[]>([]);
const categories = ref<Category[]>([]);
const tags = ref<Tag[]>([]);
const tagFilter = ref("");
const search = ref("");
const favoriteOnly = ref(false);
const categoryFilter = ref("");
const message = ref("");
const error = ref("");
const showForm = ref(false);
const showAdmin = ref(false);
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

const statusLabels: Record<string, string> = {
  unknown: "Desconocido",
  online: "Online",
  offline: "Offline",
  warning: "Atención",
};

const totalResources = computed(() => resources.value.length);

const groupedResources = computed(() => {
  const groups = new Map<number | null, { id: number | null; name: string; resources: Resource[] }>();
  for (const resource of resources.value) {
    const existing = groups.get(resource.category_id);
    if (existing) {
      existing.resources.push(resource);
      continue;
    }
    const category = categories.value.find((item) => item.id === resource.category_id);
    groups.set(resource.category_id, {
      id: resource.category_id,
      name: category?.name ?? "Sin categoría",
      resources: [resource],
    });
  }

  return [...groups.values()].sort((a, b) => {
    if (a.id === null) return 1;
    if (b.id === null) return -1;
    return a.name.localeCompare(b.name, "es");
  });
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
  if (tagFilter.value) params.set("tag", tagFilter.value);

  const [resourcesResponse, categoriesResponse, tagsResponse] = await Promise.all([
    fetch("/api/v1/resources?" + params.toString(), { cache: "no-store" }),
    fetch("/api/v1/categories", { cache: "no-store" }),
    fetch("/api/v1/tags", { cache: "no-store" }),
  ]);

  if (!resourcesResponse.ok || !categoriesResponse.ok || !tagsResponse.ok) {
    throw new Error("No se pudieron cargar los recursos.");
  }

  resources.value = await resourcesResponse.json();
  categories.value = await categoriesResponse.json();
  tags.value = await tagsResponse.json();
}

async function loadSession() {
  const response = await fetch("/api/v1/auth/me", { cache: "no-store" });
  const data = await response.json();
  authenticated.value = data.authenticated;
  username.value = data.username ?? "";
  role.value = data.role ?? "";
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
  });

  if (!response.ok) {
    error.value = "No se pudo iniciar sesión.";
    return;
  }

  const result = await response.json();
  if (!result.authenticated) {
    error.value = result.error ?? "No se pudo iniciar sesión.";
    return;
  }

  error.value = "";
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

async function logout() {
  await fetch("/api/v1/auth/logout", {
    method: "POST",
    headers: { "X-CSRF-Token": csrfToken() },
  });
  authenticated.value = false;
  resources.value = [];
  showAdmin.value = false;
  showForm.value = false;
}
 
onMounted(loadSession);
</script>

<template>
  <main class="app portal-app">
    <section class="panel">
      <header class="topbar portal-topbar">
        <div class="brand">
          <div class="brand-mark" aria-hidden="true">CH</div>
          <div>
            <p class="eyebrow">ControlHub</p>
            <h1>Mis accesos</h1>
          </div>
        </div>
        <div v-if="authenticated" class="session">
          <button v-if="role === 'admin'" class="admin-access" type="button" title="Nuevo recurso" aria-label="Crear recurso" @click="openCreate">+</button>
          <button v-if="role === 'admin'" class="admin-access" type="button" title="Administración" aria-label="Abrir administración" @click="showAdmin = true">⚙</button>
          <button class="ghost" type="button" @click="logout">Salir</button>
        </div>
      </header>

      <template v-if="loading">
        <div class="loading-card">Cargando ControlHub…</div>
      </template>

      <template v-else-if="!authenticated">
        <section class="login-shell">
          <div>
            <p class="eyebrow">Acceso privado</p>
            <h2>Tu centro de servicios</h2>
            <p>Inicia sesión para acceder a tus recursos y accesos directos.</p>
          </div>
          <form class="form login-form" @submit.prevent="login">
            <label>Usuario<input name="username" autocomplete="username" required /></label>
            <label>Contraseña<input name="password" type="password" autocomplete="current-password" required /></label>
            <button type="submit">Iniciar sesión</button>
          </form>
        </section>
      </template>

      <template v-else>
        <section class="portal-intro">
          <div>
            <h2>Accesos directos</h2>
            <p>{{ totalResources }} {{ totalResources === 1 ? "recurso disponible" : "recursos disponibles" }}</p>
          </div>
        </section>

        <section class="directory-toolbar" aria-label="Buscar y filtrar accesos">
          <label class="search-field directory-search">
            <span aria-hidden="true">⌕</span>
            <input v-model="search" type="search" placeholder="Buscar…" @input="loadData" />
          </label>
          <select v-model="categoryFilter" aria-label="Filtrar por categoría" @change="loadData">
            <option value="">Todas</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
          </select>
          <select v-model="tagFilter" aria-label="Filtrar por tag" @change="loadData">
            <option value="">Todos</option>
            <option v-for="tag in tags" :key="tag.id" :value="tag.name">{{ tag.name }}</option>
          </select>
          <label class="directory-favorite">
            <input v-model="favoriteOnly" type="checkbox" @change="loadData" />
            <span>★</span>
          </label>
        </section>

        <section v-if="groupedResources.length" class="directory">
          <section v-for="group in groupedResources" :key="group.id ?? 'uncategorized'" class="directory-section">
            <div class="directory-heading">
              <h2>{{ group.name }}</h2>
              <span>{{ group.resources.length }}</span>
            </div>
            <div class="directory-grid">
              <article v-for="resource in group.resources" :key="resource.id" class="directory-card">
                <a v-if="resource.url" class="directory-link" :href="resource.url" target="_blank" rel="noopener noreferrer" :aria-label="'Abrir ' + resource.name">
                  <div class="directory-icon" aria-hidden="true">{{ resource.icon || "◆" }}</div>
                  <div class="directory-name">{{ resource.name }}</div>
                  <div v-if="resource.description" class="directory-description">{{ resource.description }}</div>
                  <div class="directory-meta">
                    <span v-if="resource.status !== 'unknown'" :class="['directory-status', resource.status]">
                      <span class="status-dot" aria-hidden="true"></span>{{ statusLabels[resource.status] || resource.status }}
                    </span>
                    <span v-if="resource.favorite" class="directory-star" aria-label="Favorito">★</span>
                  </div>
                </a>
                <div v-else class="directory-link directory-link-static">
                  <div class="directory-icon" aria-hidden="true">{{ resource.icon || "◆" }}</div>
                  <div class="directory-name">{{ resource.name }}</div>
                  <div v-if="resource.description" class="directory-description">{{ resource.description }}</div>
                  <div class="directory-meta">
                    <span v-if="resource.host" class="directory-host">{{ resource.host }}{{ resource.port ? ":" + resource.port : "" }}</span>
                    <span v-if="resource.favorite" class="directory-star" aria-label="Favorito">★</span>
                  </div>
                </div>
                <div v-if="role === 'admin'" class="directory-admin-actions">
                  <button type="button" @click="openEdit(resource)">Editar</button>
                  <button type="button" class="danger" @click="removeResource(resource)">Eliminar</button>
                </div>
              </article>
            </div>
          </section>
        </section>

        <div v-else class="empty directory-empty">
          <div class="empty-icon" aria-hidden="true">◆</div>
          <h2>No hay accesos</h2>
          <p>Aún no hay recursos que coincidan con la búsqueda o los filtros.</p>
          <button v-if="role === 'admin'" type="button" @click="openCreate">Crear primer recurso</button>
        </div>

        <p v-if="message" class="message">{{ message }}</p>
        <p v-if="error" class="error">{{ error }}</p>
        <AdminPanel v-if="showAdmin" @close="showAdmin = false" />
      </template>
    </section>

    <div v-if="showForm" class="modal-backdrop" @click.self="showForm = false">
      <section class="modal resource-modal" role="dialog" aria-modal="true" aria-labelledby="resource-modal-title">
        <header class="modal-head">
          <div>
            <p class="eyebrow">Administración de recursos</p>
            <h2 id="resource-modal-title">{{ editingId ? "Editar recurso" : "Nuevo recurso" }}</h2>
          </div>
          <button class="icon-button" type="button" aria-label="Cerrar" @click="showForm = false">×</button>
        </header>
        <form class="form" @submit.prevent="saveResource">
          <label>Nombre<input v-model="form.name" required maxlength="200" /></label>
          <label>Descripción<textarea v-model="form.description" rows="2" /></label>
          <div class="form-grid">
            <label>Tipo
              <select v-model="form.resource_type">
                <option value="web">Web</option><option value="server">Servidor</option><option value="ssh">SSH</option><option value="service">Servicio</option><option value="database">Base de datos</option><option value="git">Git</option><option value="cloud">Cloud</option><option value="other">Otro</option>
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
            <label>Icono<input v-model="form.icon" placeholder="🌐" /></label>
          </div>
          <label>Estado
            <select v-model="form.status">
              <option value="unknown">Desconocido</option><option value="online">Online</option><option value="offline">Offline</option><option value="warning">Atención</option>
            </select>
          </label>
          <label>Tags<input v-model="form.tags" placeholder="producción, linux, web" /></label>
          <label>Notas<textarea v-model="form.notes" rows="3" /></label>
          <label class="check"><input v-model="form.favorite" type="checkbox" /> Favorito</label>
          <div class="modal-actions">
            <button class="secondary" type="button" @click="showForm = false">Cancelar</button>
            <button type="submit">Guardar recurso</button>
          </div>
        </form>
      </section>
    </div>
  </main>
</template>