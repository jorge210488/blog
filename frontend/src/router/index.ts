import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import ResourcesView from "../views/ResourcesView.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/resources", component: ResourcesView }, // Nueva ruta
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
