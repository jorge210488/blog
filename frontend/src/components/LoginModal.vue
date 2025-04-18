<script setup lang="ts">
import { ref, onMounted } from "vue";
import { login } from "../services/authService";
import { useUserStore } from "../store/userStore";
import { loginWithGoogle } from "../services/googleAuthService";
import { useToast } from "vue-toastification";
import { useRouter } from "vue-router";

const emit = defineEmits(["close"]);
const userStore = useUserStore();
const toast = useToast();
const router = useRouter();

const loginData = ref({
  email: "",
  password: "",
});

const errorMessage = ref("");

const handleLogin = async () => {
  try {
    const userData = await login(
      loginData.value.email,
      loginData.value.password
    );

    userStore.setUser(
      userData.access,
      userData.user.first_name,
      userData.user.last_name,
      userData.user.img_url || null
    );

    emit("close");
    router.push("/posts");
  } catch (error) {
    toast.error("Invalid email or password.");
  }
};

const closeModal = () => {
  emit("close");
};

const handleGoogleLogin = async (token: string) => {
  try {
    const userData = await loginWithGoogle(token);

    userStore.setUser(
      userData.access,
      userData.user.first_name,
      userData.user.last_name,
      userData.user.img_url || null
    );

    emit("close");
    router.push("/posts");
  } catch (error) {
    toast.error("Google login failed.");
  }
};

onMounted(() => {
  // @ts-ignore
  if (window.google) {
    // @ts-ignore
    window.google.accounts.id.initialize({
      client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
      callback: async (response: any) => {
        const token = response.credential;
        await handleGoogleLogin(token);
      },
      locale: "en",
    });

    // Renderizar el botón en el div
    // @ts-ignore
    window.google.accounts.id.renderButton(
      document.getElementById("google-button"),
      {
        theme: "outline",
        size: "large",
        width: "100%",
      }
    );
  }
});
</script>

<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50"
    @click.self="closeModal"
  >
    <div
      class="bg-gray-900 text-white p-6 rounded-2xl shadow-lg"
      style="width: 300px"
    >
      <h2 class="text-xl font-semibold text-center mb-4">Login</h2>

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
        <div id="google-button" class="w-full flex justify-center"></div>

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
