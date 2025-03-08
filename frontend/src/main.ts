import { createApp } from "vue";
import { createPinia } from "pinia"; // Import Pinia
import App from "./App.vue";
import router from "./router";
import "./assets/styles/tailwind.css"; // Tailwind CSS import

const app = createApp(App);

// Use Pinia instead of Vuex
app.use(createPinia());
app.use(router);
app.mount("#app");
