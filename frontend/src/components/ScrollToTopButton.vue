<script setup lang="ts">
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
};
</script>

<template>
  <button
    @click="scrollToTop"
    class="fixed bottom-20 md:bottom-2 right-5 px-4 py-1 border border-white text-white text-xl rounded-lg hover:bg-white hover:text-black transition z-50"
  >
    ↑
  </button>
</template>
