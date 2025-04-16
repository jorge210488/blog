<script setup lang="ts">
import type { Resource } from "../../services/resourceService";
import {
  downloadResourceFile,
  deleteResource,
} from "../../services/resourceService";
import { useUserStore } from "../../store/userStore";
import { computed } from "vue";

// Props
const props = defineProps<{ resource: Resource }>();
const resource = props.resource;

// User store
const userStore = useUserStore();
const isOwner = computed(() => userStore.user?.id === resource.user_id);

// Eliminar recurso
const handleDelete = async () => {
  const confirmed = window.confirm(
    "¿Estás seguro de que deseas eliminar este recurso?"
  );
  if (!confirmed) return;

  const success = await deleteResource(resource.id);
  if (success) {
    alert("✅ Recurso eliminado exitosamente");
    window.location.reload(); // o emite un evento si prefieres
  } else {
    alert("❌ Ocurrió un error al eliminar el recurso");
  }
};
</script>

<template>
  <div
    class="bg-white/10 backdrop-blur-2xl border border-white/20 p-6 rounded-xl shadow-lg transition transform hover:scale-110 hover:shadow-xl"
  >
    <h3 class="text-xl font-bold text-white">{{ resource.title }}</h3>
    <p v-if="resource.description" class="text-gray-300 text-sm mt-2">
      {{ resource.description }}
    </p>

    <!-- Botones de acción -->
    <div class="mt-4 flex justify-between items-center">
      <button
        @click="downloadResourceFile(resource.id)"
        class="px-4 py-2 text-sm rounded-lg bg-white/10 hover:bg-white/20 text-blue-400 hover:text-blue-300 transition"
      >
        📥 Download
      </button>

      <button
        v-if="isOwner"
        @click="handleDelete"
        class="px-4 py-2 border border-white rounded-lg hover:bg-white hover:text-black text-white transition text-sm"
      >
        🗑️ Eliminar
      </button>
    </div>
  </div>
</template>
