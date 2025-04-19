<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getUserResources } from "../../services/resourceService"; // ✅ Importar servicio
import type { Resource } from "../../services/resourceService";

// ✅ Estado para almacenar los resources del usuario
const userResources = ref<Resource[]>([]);
const selectedResources = ref<string[]>([]);

// ✅ Emitir eventos
const emit = defineEmits(["close", "addResources"]);

// ✅ Obtener los resources del usuario al montar el componente
const fetchResources = async () => {
  try {
    userResources.value = await getUserResources();
  } catch (error) {
    console.error("Error fetching user resources:", error);
  }
};

// ✅ Alternar selección
const toggleSelection = (resourceId: string) => {
  if (selectedResources.value.includes(resourceId)) {
    selectedResources.value = selectedResources.value.filter(
      (id) => id !== resourceId
    );
  } else {
    selectedResources.value.push(resourceId);
  }
};

// ✅ Verificar si un resource está seleccionado
const isSelected = (resourceId: string) =>
  selectedResources.value.includes(resourceId);

// ✅ Confirmar selección y emitir al padre
const confirmSelection = () => {
  const selectedResourceObjects = userResources.value.filter((resource) =>
    selectedResources.value.includes(resource.id)
  );
  emit("addResources", selectedResourceObjects); // ✅ Ahora enviamos los objetos completos
  emit("close");
};

// ✅ Llamar la API cuando se monta el componente
onMounted(fetchResources);
</script>

<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
    style="z-index: 1000 !important"
  >
    <div
      class="bg-gray-900 p-6 rounded-lg shadow-lg flex flex-col"
      style="
        width: 90% !important;
        max-width: 600px !important;
        height: 80vh !important;
        max-height: 80vh !important;
        overflow: hidden !important;
      "
    >
      <h2
        class="text-white text-xl mb-4 text-center"
        style="font-size: 1rem !important"
      >
        Select Resources
      </h2>

      <div
        v-if="userResources.length > 0"
        style="
          flex: 1 !important;
          overflow-y: auto !important;
          max-height: 50vh !important;
          padding: 8px !important;
          border: 1px solid rgba(255, 255, 255, 0.2) !important;
          border-radius: 6px !important;
        "
      >
        <div
          v-for="resource in userResources"
          :key="resource.id"
          class="bg-white/20 p-2 rounded-lg shadow-lg flex items-center justify-between transition cursor-pointer"
          :class="{ 'border-blue-500 bg-blue-500/20': isSelected(resource.id) }"
          @click="toggleSelection(resource.id)"
          style="
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            margin-bottom: 8px !important;
          "
        >
          <span
            class="text-white font-bold text-sm"
            style="font-size: 0.85rem !important"
          >
            {{ resource.title }}
          </span>

          <span
            class="text-gray-300 text-xs"
            style="font-size: 0.75rem !important"
          >
            {{ resource.tool }}
          </span>

          <span
            class="text-blue-400 font-semibold text-sm"
            style="font-size: 0.85rem !important"
          >
            {{ isSelected(resource.id) ? "✔ Selected" : "Select" }}
          </span>
        </div>
      </div>

      <p
        v-else
        class="text-gray-300 text-center"
        style="font-size: 0.9rem !important"
      >
        No resources found.
      </p>

      <div class="flex justify-between mt-4">
        <button
          @click="confirmSelection"
          class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-700"
          style="font-size: 0.9rem !important"
        >
          Add Resources
        </button>
        <button
          @click="$emit('close')"
          class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-700"
          style="font-size: 0.9rem !important"
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>
