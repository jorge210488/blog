import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "../store/userStore";
import Home from "../views/Home.vue";
import ResourcesView from "../views/ResourcesView.vue";
import CategoriesView from "../views/CategoriesView.vue";
import PostForm from "../views/PostForm.vue";
import PostView from "../views/PostView.vue";
import CategoryPostsView from "../views/CategoryPostsView.vue";
import MyPostView from "../views/MyPostView.vue";
import PostDetailView from "../views/PostDetailView.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/categories", component: CategoriesView },
  {
    path: "/resources",
    component: ResourcesView,
    meta: { requiresAuth: true },
  },
  {
    path: "/create-post",
    component: PostForm,
    meta: { requiresAuth: true },
  },
  {
    path: "/posts/:slug",
    component: PostDetailView,
  },
  {
    path: "/posts",
    component: PostView,
  },
  {
    path: "/category/:slug", // ✅ Nueva ruta dinámica por slug
    component: CategoryPostsView,
  },
  {
    path: "/my-posts",
    component: MyPostView,
    meta: { requiresAuth: true }, // 🔒 Solo para usuarios logueados
  },
  {
    path: "/auth-callback",
    name: "AuthCallback",
    component: () => import("../views/AuthCallbackView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// ✅ Middleware para proteger rutas
router.beforeEach((to, _from, next) => {
  const userStore = useUserStore();
  const isAuthenticated = !!userStore.token;

  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/"); // 🔥 Solo redirige al Home
  } else {
    next(); // ✅ Permite la navegación normalmente
  }
});

export default router;
