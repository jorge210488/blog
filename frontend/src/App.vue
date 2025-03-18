<template>
  <div>
    <Navbar />
    <!-- ✅ Se usa el Navbar como componente -->
    <router-view></router-view>
  </div>
</template>

<script setup lang="ts">
import Navbar from "./components/NavBar.vue"; // ✅ Importado correctamente
</script>
