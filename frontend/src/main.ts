import { createApp } from "vue";
import { createPinia } from "pinia";
import { createI18n } from "vue-i18n";
import App from "./App.vue";
import "./style.css";

const i18n = createI18n({
  legacy: false,
  locale: "es",
  messages: {
    es: {
      appTitle: "ControlHub",
      welcome: "Centro de control",
      foundation: "Base inicial preparada para la V1.",
    },
  },
});

createApp(App).use(createPinia()).use(i18n).mount("#app");
