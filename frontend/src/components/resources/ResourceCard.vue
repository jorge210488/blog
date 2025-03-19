<script setup lang="ts">
import type { PropType } from "vue";

// Definimos la estructura esperada del recurso
interface Resource {
  id: string;
  title: string;
  description?: string;
  file: string;
}

// Definimos las props con tipado estricto
defineProps({
  resource: {
    type: Object as PropType<Resource>,
    required: true,
  },
});
</script>

<template>
  <div
    class="bg-white/10 backdrop-blur-2xl border border-white/20 p-6 rounded-xl shadow-lg transition transform hover:scale-110 hover:shadow-xl"
  >
    <h3 class="text-xl font-bold text-white">{{ resource.title }}</h3>
    <p v-if="resource.description" class="text-gray-300 text-sm mt-2">
      {{ resource.description }}
    </p>
    <a
      :href="resource.file"
      target="_blank"
      class="block mt-4 text-blue-400 hover:text-blue-300 font-semibold"
    >
      📥 Descargar Recurso
    </a>
  </div>
</template>
