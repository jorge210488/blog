<script setup lang="ts">
import { ref } from "vue";

// Simulación de usuario autenticado (puedes reemplazar esto con Vuex/Pinia)
const isAuthenticated = ref(true);
const isAuthor = ref(true); // Solo los autores pueden escribir posts
const username = ref("JohnDoe");
const profilePicture = ref("/profile.jpg");

// Control del menú desplegable
const showDropdown = ref(false);
const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value;
};

// Menú de navegación
const menuItems = ["Home", "Categories", "Blog"];
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
          v-for="item in menuItems"
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
          <a href="/profile" class="block px-4 py-2 hover:bg-gray-100"
            >👤 Profile</a
          >
          <a href="/settings" class="block px-4 py-2 hover:bg-gray-100"
            >⚙️ Settings</a
          >
          <a
            href="/logout"
            class="block px-4 py-2 hover:bg-red-500 text-red-700"
            >🚪 Logout</a
          >
        </div>
      </div>

      <!-- Botón de login si el usuario no está autenticado -->
      <div v-else>
        <a
          href="/login"
          class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700"
        >
          Sign In
        </a>
      </div>
    </div>
  </nav>
</template>
