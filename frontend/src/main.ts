import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./assets/styles/tailwind.css";
import Toast, { type PluginOptions, POSITION } from "vue-toastification";
import "vue-toastification/dist/index.css";
import createGtag from "vue-gtag-next";

const options: PluginOptions = {
  position: POSITION.TOP_RIGHT,
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: "button",
  icon: true,
};

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

const app = createApp(App);
app.use(Toast, options);
app.use(pinia);
app.use(router);

if (import.meta.env.MODE === "production") {
  app.use(createGtag, {
    property: {
      id: import.meta.env.VITE_GA_MEASUREMENT_ID || "",
    },
  });
}

app.mount("#app");
