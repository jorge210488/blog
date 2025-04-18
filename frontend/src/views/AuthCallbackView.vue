<script setup lang="ts">
import { onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useUserStore } from "../store/userStore";

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();

onMounted(() => {
  const token = route.query.token as string;
  const first_name = route.query.first_name as string;
  const last_name = route.query.last_name as string;
  const img_url = route.query.img_url as string | undefined;

  // ✅ Agregar logs para verificar qué llega en la query
  console.log("🔍 Google Auth Token:", token);
  console.log("👤 First Name:", first_name);
  console.log("👤 Last Name:", last_name);
  console.log("🖼️ Image URL:", img_url);

  if (token) {
    userStore.setUser(token, first_name, last_name, img_url || null);
    router.push("/"); // redirigimos al inicio o a donde quieras
  } else {
    alert("Google login failed.");
    router.push("/login");
  }
});
</script>

<template>
  <div class="text-white text-center mt-10">Authenticating with Google...</div>
</template>
