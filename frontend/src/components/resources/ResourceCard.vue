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
  <div class="bg-[#1A2B40] p-4 rounded-lg shadow-md">
    <h3 class="text-lg font-bold">{{ resource.title }}</h3>
    <p v-if="resource.description" class="text-gray-400 text-sm">
      {{ resource.description }}
    </p>
    <a
      :href="resource.file"
      target="_blank"
      class="block mt-2 text-blue-400 hover:text-blue-300"
    >
      📥 Descargar Recurso
    </a>
  </div>
</template>
