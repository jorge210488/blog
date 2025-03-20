<script setup lang="ts">
import { ref, defineEmits } from "vue";

const search = ref("");
const emit = defineEmits(["filter"]);

const applyFilters = () => {
  emit("filter", search.value);
};
</script>

<template>
  <div
    class="bg-black/40 backdrop-blur-xl border border-white/30 p-4 rounded-lg shadow-lg flex flex-col sm:flex-row sm:items-center gap-4 mx-auto md:w-3/4"
  >
    <!-- Búsqueda -->
    <input
      v-model="search"
      @input="applyFilters"
      type="text"
      placeholder="🔎 Search Category..."
      class="w-full p-3 rounded-md bg-transparent border border-white/40 text-white placeholder-gray-400 focus:outline-none focus:border-blue-400"
    />
  </div>
</template>
