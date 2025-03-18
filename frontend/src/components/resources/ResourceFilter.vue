<script setup lang="ts">
import { ref, defineEmits } from "vue";

const search = ref("");
const selectedTool = ref("");
const sortBy = ref("latest");

const emit = defineEmits(["filter"]);

const applyFilters = () => {
  emit("filter", {
    search: search.value,
    tool: selectedTool.value,
    sortBy: sortBy.value,
  });
};
</script>

<template>
  <div
    class="bg-[#12263A] p-4 rounded-lg shadow-lg flex flex-col sm:flex-row sm:items-center gap-4"
  >
    <input
      v-model="search"
      @input="applyFilters"
      type="text"
      placeholder="🔎 Buscar recurso..."
      class="w-full p-2 rounded-md text-black"
    />

    <select
      v-model="selectedTool"
      @change="applyFilters"
      class="p-2 rounded-md text-black"
    >
      <option value="">Todas las herramientas</option>
      <option value="Relevance AI">Relevance AI</option>
      <option value="Make">Make</option>
      <option value="n8n">n8n</option>
      <option value="Other">Otras</option>
    </select>

    <select
      v-model="sortBy"
      @change="applyFilters"
      class="p-2 rounded-md text-black"
    >
      <option value="latest">Más recientes</option>
      <option value="oldest">Más antiguos</option>
    </select>
  </div>
</template>
