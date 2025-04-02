<!-- components/posts/ResourcesModal.vue -->
<script setup lang="ts">
import { ref, watch } from "vue";

defineProps<{
  resources: {
    id: string;
    title: string;
    description?: string;
    file: string;
  }[];
  show: boolean;
}>();

const emit = defineEmits(["close"]);
</script>

<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-black/70 flex items-center justify-center z-50"
    @click.self="emit('close')"
  >
    <div
      class="bg-[#0f1d2a] w-full max-w-xl rounded-xl p-6 shadow-xl text-white"
    >
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold">📎 Recursos del Post</h2>
        <button
          @click="emit('close')"
          class="text-white hover:text-red-400 text-xl"
        >
          ✖
        </button>
      </div>

      <div v-if="resources.length" class="space-y-4">
        <div
          v-for="resource in resources"
          :key="resource.id"
          class="border-t border-white/10 pt-3"
        >
          <h3 class="text-lg font-semibold">{{ resource.title }}</h3>
          <p class="text-sm text-white/80 mb-2">{{ resource.description }}</p>
          <a
            :href="resource.file"
            target="_blank"
            download
            class="inline-block px-3 py-1 bg-white/10 rounded hover:bg-white/20 text-sm"
          >
            ⬇️ Descargar archivo
          </a>
        </div>
      </div>

      <div v-else class="text-center text-white/60">
        No hay recursos disponibles.
      </div>
    </div>
  </div>
</template>
