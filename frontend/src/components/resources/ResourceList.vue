<script setup lang="ts">
import ResourceCard from "./ResourceCard.vue";
import type { PropType } from "vue";

// Definimos la estructura del recurso
interface Resource {
  id: string;
  title: string;
  description?: string;
  file: string;
}

defineProps({
  resources: {
    type: Array as PropType<Resource[]>,
    required: true,
  },
});
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-6 mb-20">
    <ResourceCard
      v-for="resource in resources"
      :key="resource.id"
      :resource="resource"
    />
  </div>
</template>
