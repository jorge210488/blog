<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getUserResources } from "../../services/resourceService"; // ✅ Importar servicio

interface Resource {
  id: string;
  title: string;
  description: string;
  tool: string;
}

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
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div
      class="bg-gray-900 p-6 rounded-lg shadow-lg w-[90%] sm:w-[80%] md:w-[70%] lg:w-[60%] max-h-[80vh] overflow-y-auto"
    >
      <h2 class="text-white text-xl mb-4 text-center">Select Resources</h2>

      <!-- Lista de Resources -->
      <div v-if="userResources.length > 0" class="flex flex-col gap-3">
        <div
          v-for="resource in userResources"
          :key="resource.id"
          class="bg-white/20 backdrop-blur-3xl border border-white/40 p-2 rounded-lg shadow-lg w-full flex items-center justify-between transition transform hover:scale-105 hover:shadow-xl cursor-pointer"
          :class="{ 'border-blue-500 bg-blue-500/20': isSelected(resource.id) }"
          @click="toggleSelection(resource.id)"
        >
          <!-- Resource title -->
          <span class="text-white font-bold text-sm">{{ resource.title }}</span>

          <!-- Tool name -->
          <span class="text-gray-300 text-xs">{{ resource.tool }}</span>

          <!-- Checkbox -->
          <span class="text-blue-400 font-semibold text-sm">
            {{ isSelected(resource.id) ? "✔ Selected" : "Select" }}
          </span>
        </div>
      </div>

      <!-- Si no hay resources -->
      <p v-else class="text-gray-300 text-center">No resources found.</p>

      <!-- Botones -->
      <div class="flex justify-between mt-6">
        <button
          @click="confirmSelection"
          class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Add Resources
        </button>
        <button
          @click="$emit('close')"
          class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-700"
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>
