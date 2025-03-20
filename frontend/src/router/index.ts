import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "../store/userStore";
import Home from "../views/Home.vue";
import ResourcesView from "../views/ResourcesView.vue";
import CategoriesView from "../views/CategoriesView.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/categories", component: CategoriesView },
  {
    path: "/resources",
    component: ResourcesView,
    meta: { requiresAuth: true },
  }, // 🔒 Ruta protegida
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// ✅ Middleware para proteger rutas
router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  const isAuthenticated = !!userStore.token; // Comprueba si hay sesión activa

  if (to.meta.requiresAuth && !isAuthenticated) {
    userStore.showLoginModal = true; // 🚀 En lugar de redirigir, abre el modal de login
    next(false); // 🚫 Bloquea la navegación
  } else {
    next(); // ✅ Permite la navegación
  }
});

export default router;
