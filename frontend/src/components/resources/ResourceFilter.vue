<script setup lang="ts">
import { ref, defineEmits } from "vue";

// Estados de los filtros
const search = ref("");
const selectedTool = ref("");
const sortBy = ref<"-updated_at" | "updated_at">("-updated_at"); // Tipo correcto

const emit = defineEmits(["filter"]);

// Función para aplicar los filtros y emitirlos al `resourcesView`
const applyFilters = () => {
  emit("filter", {
    search: search.value || undefined,
    tool: selectedTool.value || undefined,
    sortBy: sortBy.value, // Ahora TypeScript reconoce los valores correctos
  });
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
      placeholder="🔎 Search Resource..."
      class="w-full p-3 rounded-md bg-transparent border border-white/40 text-white placeholder-gray-400 focus:outline-none focus:border-blue-400"
    />

    <!-- Filtrar por herramienta -->
    <select v-model="selectedTool" @change="applyFilters" class="custom-select">
      <option value="">All Tools</option>
      <option value="Relevance AI">Relevance AI</option>
      <option value="Make">Make</option>
      <option value="n8n">n8n</option>
      <option value="Other">Other</option>
    </select>

    <!-- Ordenar por fecha -->
    <select v-model="sortBy" @change="applyFilters" class="custom-select">
      <option :value="'-updated_at'">Newest</option>
      <option :value="'updated_at'">Oldest</option>
    </select>
  </div>
</template>

<style scoped>
/* Aplica fondo transparente y bordes correctos */
.custom-select {
  background-color: transparent !important; /* 🔥 Clave para evitar fondo blanco */
  border: 1px solid rgba(255, 255, 255, 0.4);
  color: white;
  padding: 12px;
  border-radius: 6px;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  cursor: pointer;
}

/* Forzar opciones a ser oscuras */
.custom-select option {
  background-color: black !important;
  color: white !important;
}

/* Cuando está enfocado */
.custom-select:focus {
  border-color: #4299e1;
  outline: none;
}
</style>
