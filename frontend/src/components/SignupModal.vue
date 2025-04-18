<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useUserStore } from "../store/userStore";
import { register } from "../services/authService";
import { loginWithGoogle } from "../services/googleAuthService";
import { useToast } from "vue-toastification";
import { useRouter } from "vue-router";

const emit = defineEmits(["close"]);
const userStore = useUserStore();
const toast = useToast();
const router = useRouter();

const signupData = ref({
  first_name: "",
  last_name: "",
  email: "",
  password: "",
});

const successMessage = ref("");
const errorMessage = ref("");

const handleRegister = async () => {
  try {
    console.log("Intentando registro con:", signupData.value);

    await register({
      ...signupData.value,
      role: "author",
    });

    // ✅ Mostrar mensaje de éxito en lugar de hacer login
    successMessage.value =
      "Account created! Please check your email to verify your account.";
  } catch (error) {
    console.error("Error en registro:", error);
    errorMessage.value = (error as Error).message;
  }
};

const closeModal = () => {
  emit("close");
};

const signupWithGoogle = async (token: string) => {
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
    toast.error("Google signup failed.");
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
        await signupWithGoogle(token);
      },
      locale: "en",
    });

    // @ts-ignore
    window.google.accounts.id.renderButton(
      document.getElementById("google-signup-button"),
      {
        theme: "outline",
        size: "large",
        width: "100%",
        text: "signup_with",
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
      <h2 class="text-xl font-semibold text-center mb-4">Sign Up</h2>

      <div v-if="errorMessage" class="text-red-500 text-sm text-center mb-2">
        {{ errorMessage }}
      </div>

      <div
        v-if="successMessage"
        class="text-green-400 text-sm text-center mb-2"
      >
        {{ successMessage }}
      </div>

      <div class="space-y-4" v-if="!successMessage">
        <div>
          <label class="block text-sm text-gray-400">First Name</label>
          <input
            type="text"
            v-model="signupData.first_name"
            class="w-full px-3 py-2 bg-gray-800 rounded-lg text-white outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block text-sm text-gray-400">Last Name</label>
          <input
            type="text"
            v-model="signupData.last_name"
            class="w-full px-3 py-2 bg-gray-800 rounded-lg text-white outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block text-sm text-gray-400">Email</label>
          <input
            type="email"
            v-model="signupData.email"
            class="w-full px-3 py-2 bg-gray-800 rounded-lg text-white outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block text-sm text-gray-400">Password</label>
          <input
            type="password"
            v-model="signupData.password"
            class="w-full px-3 py-2 bg-gray-800 rounded-lg text-white outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <button
          @click="handleRegister"
          class="w-full px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
        >
          Create Account
        </button>

        <div class="flex items-center my-4">
          <div class="w-full border-t border-gray-500"></div>
          <span class="px-3 text-gray-400 text-sm">or</span>
          <div class="w-full border-t border-gray-500"></div>
        </div>

        <div id="google-signup-button" class="w-full flex justify-center"></div>
      </div>

      <button
        @click="closeModal"
        class="w-full px-4 py-2 mt-4 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition"
      >
        {{ successMessage ? "Close" : "Cancel" }}
      </button>
    </div>
  </div>
</template>
