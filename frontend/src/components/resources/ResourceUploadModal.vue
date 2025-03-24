<script setup lang="ts">
import { ref } from "vue";
import { useToast } from "vue-toastification";

const toast = useToast();
const emit = defineEmits(["close", "upload"]);

const jsonFile = ref<File | null>(null);
const title = ref<string>("");
const description = ref<string>("");
const tool = ref<string>("Relevance AI");

// Opciones de herramientas según el modelo
const toolOptions = ["Relevance AI", "Make", "n8n", "Other"];

// ✅ Manejar archivo JSON seleccionado
const handleFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (!input.files || input.files.length === 0) return;

  const file = input.files[0];
  if (!file.name.endsWith(".json")) {
    toast.error("Solo se permiten archivos JSON. ❌");
    return;
  }

  jsonFile.value = file; // Solo se permite un archivo JSON
};

// ✅ Subir JSON al backend
const uploadFile = () => {
  if (!jsonFile.value) {
    toast.error("Debes seleccionar un archivo JSON. ❌");
    return;
  }
  if (!title.value.trim()) {
    toast.error("El título es obligatorio. ❌");
    return;
  }
  if (!description.value.trim()) {
    toast.error("La descripción es obligatoria. ❌");
    return;
  }
  if (!tool.value.trim()) {
    toast.error("Debes seleccionar una herramienta. ❌");
    return;
  }

  // ✅ Crear objeto de recurso
  const resource = {
    id: crypto.randomUUID(), // Simula el ID generado por el backend
    title: title.value,
    description: description.value,
    tool: tool.value,
    file: jsonFile.value,
  };

  emit("upload", resource);
  toast.success("Recurso subido exitosamente! ✅");

  // ✅ Limpiar formulario para permitir más subidas
  jsonFile.value = null;
  title.value = "";
  description.value = "";
  tool.value = "Relevance AI";
};
</script>

<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
  >
    <div class="bg-gray-900 p-6 rounded-lg shadow-lg w-96">
      <h2 class="text-white text-xl mb-4">Subir Recurso JSON</h2>

      <!-- Título -->
      <div class="mb-4">
        <label class="text-white">Título:</label>
        <input
          type="text"
          v-model="title"
          class="w-full text-black p-2 rounded"
          placeholder="Escribe un título"
        />
      </div>

      <!-- Descripción -->
      <div class="mb-4">
        <label class="text-white">Descripción:</label>
        <textarea
          v-model="description"
          class="w-full text-black p-2 rounded"
          placeholder="Agrega una descripción"
        ></textarea>
      </div>

      <!-- Seleccionar Herramienta -->
      <div class="mb-4">
        <label class="text-white">Herramienta:</label>
        <select v-model="tool" class="w-full text-black p-2 rounded">
          <option v-for="option in toolOptions" :key="option" :value="option">
            {{ option }}
          </option>
        </select>
      </div>

      <!-- Subir JSON -->
      <div class="mb-4">
        <label class="text-white">Archivo JSON:</label>
        <input
          type="file"
          accept=".json"
          @change="handleFileChange"
          class="w-full text-white"
        />
      </div>

      <!-- Botones -->
      <div class="flex justify-between mt-4">
        <button
          @click="uploadFile"
          class="bg-green-500 text-white px-4 py-2 rounded"
        >
          Subir
        </button>
        <button
          @click="$emit('close')"
          class="bg-red-500 text-white px-4 py-2 rounded"
        >
          Cerrar
        </button>
      </div>
    </div>
  </div>
</template>
