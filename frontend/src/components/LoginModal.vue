<script setup lang="ts">
import { ref } from "vue";
import { login } from "../services/authService";
import { useUserStore } from "../store/userStore";

const emit = defineEmits(["close"]);
const userStore = useUserStore();

const loginData = ref({
  email: "",
  password: "",
});

const errorMessage = ref("");

const handleLogin = async () => {
  try {
    console.log("Intentando login con:", loginData.value);

    const userData = await login(
      loginData.value.email,
      loginData.value.password
    );

    console.log("Datos recibidos:", userData);

    userStore.setUser(
      userData.access,
      userData.user.first_name,
      userData.user.last_name,
      userData.user.img_url || null
    );

    emit("close");
  } catch (error) {
    console.error("Error en login:", error);
    errorMessage.value = (error as Error).message;
  }
};

const closeModal = () => {
  emit("close");
};

const loginWithGoogle = () => {
  console.log("Login with Google");
};
</script>

<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50"
    @click.self="closeModal"
  >
    <div
      class="bg-gray-900 text-white p-6 rounded-2xl shadow-lg"
      style="width: 380px !important; max-width: none !important"
    >
      <h2 class="text-xl font-semibold text-center mb-4">Login</h2>

      <!-- Mensaje de error -->
      <div v-if="errorMessage" class="text-red-500 text-sm text-center mb-2">
        {{ errorMessage }}
      </div>

      <div class="space-y-4">
        <div>
          <label class="block text-sm text-gray-400">Email</label>
          <input
            type="email"
            v-model="loginData.email"
            class="w-full px-3 py-2 bg-gray-800 rounded-lg text-white outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block text-sm text-gray-400">Password</label>
          <input
            type="password"
            v-model="loginData.password"
            class="w-full px-3 py-2 bg-gray-800 rounded-lg text-white outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <!-- Botón de login -->
        <button
          @click="handleLogin"
          class="w-full px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
        >
          Login
        </button>

        <!-- Separador -->
        <div class="flex items-center my-4">
          <div class="w-full border-t border-gray-500"></div>
          <span class="px-3 text-gray-400 text-sm">or</span>
          <div class="w-full border-t border-gray-500"></div>
        </div>

        <!-- Botón de Google -->
        <button
          @click="loginWithGoogle"
          class="w-full flex items-center justify-center px-4 py-2 bg-white text-gray-900 rounded-lg hover:bg-gray-300 transition"
        >
          <img src="/google-icon.svg" alt="Google" class="w-5 h-5 mr-2" />
          Sign in with Google
        </button>

        <!-- Botón de cerrar -->
        <button
          @click="closeModal"
          class="w-full px-4 py-2 mt-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition"
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>
