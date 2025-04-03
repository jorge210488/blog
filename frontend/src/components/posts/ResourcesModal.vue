<script setup lang="ts">
defineProps<{
  resources: {
    id: string;
    title: string;
    description?: string;
    file: string;
    tool?: string;
  }[];
  show: boolean;
}>();

const emit = defineEmits(["close"]);
</script>

<template>
  <div
    v-if="show"
    class="fixed mt-0 mx-2 md:mt-10 inset-0 bg-black/70 flex items-center justify-center z-50"
    @click.self="emit('close')"
    @keyup.esc="emit('close')"
    tabindex="0"
  >
    <div
      class="bg-gray-900 px-6 py-2 rounded-lg shadow-lg w-[90%] max-w-[600px] max-h-[90vh] overflow-y-auto text-white"
    >
      <!-- Header -->
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold">📎 Post Resources</h2>
        <button
          @click="emit('close')"
          class="text-white hover:text-red-400 text-xl"
        >
          x
        </button>
      </div>

      <!-- Lista de recursos -->
      <div v-if="resources.length" class="space-y-4">
        <div
          v-for="resource in resources"
          :key="resource.id"
          class="bg-white/10 p-4 rounded-lg border border-white/20"
        >
          <h3 class="text-base font-semibold">{{ resource.title }}</h3>
          <p class="text-sm text-white/70 mb-2">
            {{ resource.description || "Sin descripción" }}
          </p>

          <!-- Download izquierda / Tool derecha -->
          <div class="flex justify-between items-center">
            <a
              :href="resource.file"
              target="_blank"
              download
              class="px-3 py-1 bg-blue-500 rounded hover:bg-blue-600 text-sm transition"
            >
              ⬇️ Download
            </a>
            <p v-if="resource.tool" class="text-xs text-blue-300">
              🛠️ {{ resource.tool }}
            </p>
          </div>
        </div>
      </div>

      <div v-else class="text-center text-white/60 mt-4">No Resources.</div>
    </div>
  </div>
</template>
