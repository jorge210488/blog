<template>
  <footer
    v-show="isAtBottom"
    class="fixed bottom-0 left-0 w-full z-50 bg-transparent text-white py-4 text-center transition-opacity duration-300"
  >
    Blog by Jorge Martínez —
    <a
      href="https://jorgemartinezjam.dev/"
      target="_blank"
      rel="noopener noreferrer"
      class="underline hover:text-blue-400"
    >
      Portfolio
    </a>
  </footer>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";

const isAtBottom = ref(false);

const handleScroll = () => {
  const scrollTop = window.scrollY;
  const windowHeight = window.innerHeight;
  const fullHeight = document.documentElement.scrollHeight;
  isAtBottom.value = scrollTop + windowHeight >= fullHeight - 10;
};

onMounted(() => {
  window.addEventListener("scroll", handleScroll);
  handleScroll();
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});
</script>
