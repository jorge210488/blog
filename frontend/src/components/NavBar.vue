<script setup lang="ts">
import { ref, computed } from "vue";
import Profile from "./Profile.vue";
import LoginModal from "./LoginModal.vue";
import { useUserStore } from "../store/userStore";

const userStore = useUserStore();

const isAuthenticated = computed(() => !!userStore.token);
const username = computed(() => userStore.user?.first_name || "Guest");
const profilePicture = computed(
  () => userStore.user?.img_url || "/profile3.avif"
);
const isAuthor = computed(() => userStore.user?.role === "author");

// Control del menú desplegable
const showDropdown = ref(false);
const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value;
};

// Control de modales
const showProfileModal = ref(false);
const showLoginModal = ref(false);
const openProfileModal = () => {
  showProfileModal.value = true;
};
const openLoginModal = () => {
  showLoginModal.value = true;
};

// ✅ Función para cerrar sesión
const logout = () => {
  userStore.logout();
  showDropdown.value = false;
};
</script>

<template>
  <nav class="fixed top-0 left-0 w-full z-50 bg-transparent">
    <div
      class="container mx-auto flex justify-between items-center py-4 px-6 text-white"
    >
      <!-- Logo -->
      <div class="text-lg font-bold">JAM BLOG</div>

      <!-- Menú Principal -->
      <div class="hidden md:flex space-x-6">
        <button
          v-for="item in ['Home', 'Categories', 'Blog']"
          :key="item"
          class="px-4 py-2 rounded-lg hover:bg-white hover:text-black transition"
        >
          {{ item }}
        </button>

        <!-- Mostrar "Write a Post" solo si el usuario es autor -->
        <button
          v-if="isAuthenticated && isAuthor"
          class="px-4 py-2 rounded-lg hover:bg-white hover:text-black transition"
        >
          ✍️ Write a Post
        </button>
      </div>

      <!-- Menú de usuario -->
      <div v-if="isAuthenticated" class="relative">
        <button
          @click="toggleDropdown"
          class="flex items-center space-x-2 focus:outline-none"
        >
          <img
            :src="profilePicture"
            alt="Profile"
            class="w-8 h-8 rounded-full border-2 border-white"
          />
          <span>{{ username }}</span>
        </button>

        <!-- Dropdown del usuario -->
        <div
          v-if="showDropdown"
          class="absolute right-0 mt-2 w-48 bg-white text-black rounded-lg shadow-lg py-2"
        >
          <button
            @click="openProfileModal"
            class="block px-4 py-2 hover:bg-gray-100"
          >
            👤 Profile
          </button>
          <a href="/settings" class="block px-4 py-2 hover:bg-gray-100"
            >⚙️ Settings</a
          >
          <button
            @click="logout"
            class="block px-4 py-2 hover:bg-red-500 text-red-700 w-full"
          >
            🚪 Logout
          </button>
        </div>
      </div>

      <!-- Botón de login si el usuario no está autenticado -->
      <div v-else class="flex space-x-4">
        <a
          href="/signup"
          class="px-4 py-2 border border-white rounded-lg hover:bg-white hover:text-black transition"
        >
          Sign Up
        </a>
        <button
          @click="openLoginModal"
          class="px-4 py-2 border border-white rounded-lg hover:bg-white hover:text-black transition"
        >
          Login
        </button>
      </div>
    </div>
  </nav>

  <!-- Profile Modal -->
  <Profile v-if="showProfileModal" @close="showProfileModal = false" />
  <LoginModal v-if="showLoginModal" @close="showLoginModal = false" />
</template>
