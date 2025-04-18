<template>
  <div>
    <Navbar />
    <!-- ✅ Se usa el Navbar como componente -->
    <router-view></router-view>
    <Footer />
    <ScrollToTopButton />
  </div>
</template>

<script setup lang="ts">
import Navbar from "./components/NavBar.vue"; // ✅ Importado correctamente
import Footer from "./components/Footer.vue";
import ScrollToTopButton from "./components/ScrollToTopButton.vue";
</script>
