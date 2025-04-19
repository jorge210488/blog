<script setup lang="ts">
import { ref, computed } from "vue";
import Profile from "./account/Profile.vue";
import ContactModal from "./account/ContactModal.vue";
import LoginModal from "./LoginModal.vue";
import { useUserStore } from "../store/userStore";
import { useRouter, useRoute } from "vue-router";
import SignupModal from "./SignupModal.vue";

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

const isAuthenticated = computed(() => !!userStore.token);
const username = computed(() => userStore.user?.first_name || "Guest");
const profilePicture = computed(
  () => userStore.user?.img_url || "/profile3.avif"
);
const isAuthor = computed(() => userStore.user?.role === "author");

// 🔥 Detectar si el usuario está en `/resources`
const isResourcesView = computed(() => route.path === "/resources");

// Control del menú hamburguesa en móviles
const showMobileMenu = ref(false);
const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value;
};

// Control del menú desplegable de usuario
const showDropdown = ref(false);
const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value;
};

const showProfileModal = ref(false);
const openProfileModal = () => {
  showProfileModal.value = true;
};
const showContactModal = ref(false);
const openContactModal = () => {
  showContactModal.value = true;
};

// ✅ Usar `userStore.showLoginModal`
const openLoginModal = () => {
  userStore.showLoginModal = true;
};

const showSignupModal = ref(false);
const openSignupModal = () => {
  showSignupModal.value = true;
};

// ✅ Cerrar menú móvil al hacer logout
const logout = () => {
  userStore.logout();
  showDropdown.value = false;
  showMobileMenu.value = false;
  router.push("/");
};
</script>

<template>
  <nav class="fixed top-0 left-0 w-full z-50 bg-transparent">
    <div
      class="container mx-auto flex justify-between items-center py-4 px-6 text-white"
    >
      <router-link to="/" class="text-lg font-bold">JAM BLOG</router-link>

      <!-- Menú Hamburguesa en móviles -->
      <button
        @click="toggleMobileMenu"
        class="md:hidden text-2xl focus:outline-none"
      >
        ☰
      </button>

      <!-- Menú Principal en pantallas grandes -->
      <div class="hidden md:flex space-x-6">
        <router-link
          to="/"
          class="px-4 py-2 rounded-lg hover:bg-white hover:text-black transition"
          >Home</router-link
        >
        <router-link
          to="/categories"
          class="px-4 py-2 rounded-lg hover:bg-white hover:text-black transition"
          >Categories</router-link
        >
        <router-link
          to="/posts"
          class="px-4 py-2 rounded-lg hover:bg-white hover:text-black transition"
          >Posts</router-link
        >

        <router-link
          v-if="isAuthenticated && isAuthor"
          to="/create-post"
          class="px-4 py-2 rounded-lg hover:bg-white hover:text-black transition"
        >
          ✍️ Write a Post
        </router-link>

        <!-- ✅ Bloquear acceso a `/resources` si no está autenticado -->
        <router-link
          v-if="isAuthenticated"
          to="/resources"
          class="px-4 py-2 rounded-lg hover:bg-white hover:text-black transition"
        >
          📚 Resources
        </router-link>

        <router-link
          v-if="isAuthenticated && isAuthor"
          to="/my-posts"
          class="px-4 py-2 rounded-lg hover:bg-white hover:text-black transition"
        >
          My Posts
        </router-link>
      </div>

      <!-- Menú de usuario en pantallas grandes -->
      <div v-if="isAuthenticated" class="relative hidden md:block">
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
            class="block px-4 py-2 hover:bg-gray-200"
          >
            👤 Profile
          </button>
          <button
            @click="openContactModal"
            class="block px-4 py-2 hover:bg-gray-200"
          >
            🛟 Support
          </button>
          <button
            @click="logout"
            class="block px-4 py-2 text-red-700 hover:bg-red-200 w-full text-left"
          >
            🚪 Logout
          </button>
        </div>
      </div>

      <!-- Botón de login en pantallas grandes -->
      <div v-else class="hidden md:flex space-x-4">
        <button
          @click="openSignupModal"
          class="px-4 py-2 border border-white rounded-lg hover:bg-white hover:text-black transition"
        >
          Sign Up
        </button>

        <button
          @click="openLoginModal"
          class="px-4 py-2 border border-white rounded-lg hover:bg-white hover:text-black transition"
        >
          Login
        </button>
      </div>
    </div>

    <!-- Menú móvil -->
    <transition name="fade">
      <div
        v-if="showMobileMenu"
        class="absolute top-0 left-0 w-full h-screen bg-black bg-opacity-90 flex flex-col items-center justify-center space-y-6 text-white text-lg md:hidden"
      >
        <button
          @click="toggleMobileMenu"
          class="absolute top-5 right-5 text-3xl"
        >
          ✖
        </button>

        <router-link to="/" @click="toggleMobileMenu" class="w-full text-center"
          >Home</router-link
        >
        <router-link
          to="/categories"
          @click="toggleMobileMenu"
          class="w-full text-center"
          >Categories</router-link
        >
        <router-link
          to="/posts"
          @click="toggleMobileMenu"
          class="w-full text-center"
          >Posts</router-link
        >

        <router-link
          v-if="isAuthenticated && isAuthor"
          to="/create-post"
          @click="toggleMobileMenu"
          class="w-full text-center"
        >
          ✍️ Write a Post
        </router-link>

        <!-- ✅ Bloquear acceso a `/resources` si no está autenticado -->
        <router-link
          v-if="isAuthenticated"
          to="/resources"
          @click="toggleMobileMenu"
          class="w-full text-center"
        >
          📚 Resources
        </router-link>

        <router-link
          v-if="isAuthenticated && isAuthor"
          to="/my-posts"
          @click="toggleMobileMenu"
          class="w-full text-center"
        >
          My Posts
        </router-link>

        <!-- Menú de usuario en móviles -->
        <div
          v-if="isAuthenticated"
          class="flex flex-col items-center w-full space-y-4 mt-4"
        >
          <button @click="openProfileModal" class="w-full text-center">
            👤 Profile
          </button>
          <button
            @click="
              toggleMobileMenu();
              openContactModal();
            "
            class="w-full text-center"
          >
            🛟 Support
          </button>
          <button @click="logout" class="w-full text-center text-red-500">
            🚪 Logout
          </button>
        </div>

        <!-- Menú de login/signup en móviles -->
        <div v-else class="flex flex-col items-center w-full space-y-4 mt-4">
          <button
            @click="
              toggleMobileMenu();
              openSignupModal();
            "
            class="w-full text-center"
          >
            Sign Up
          </button>

          <button @click="openLoginModal" class="w-full text-center">
            Login
          </button>
        </div>
      </div>
    </transition>
  </nav>

  <!-- Profile Modal -->
  <Profile v-if="showProfileModal" @close="showProfileModal = false" />
  <ContactModal v-if="showContactModal" @close="showContactModal = false" />
  <LoginModal
    v-if="userStore.showLoginModal"
    @close="userStore.showLoginModal = false"
  />
  <SignupModal v-if="showSignupModal" @close="showSignupModal = false" />
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
