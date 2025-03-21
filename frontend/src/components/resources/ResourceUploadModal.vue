<script setup lang="ts">
import { ref } from "vue";

const emit = defineEmits(["close", "upload"]);
const jsonFile = ref<File | null>(null);
const imageFiles = ref<File[]>([]);

// Manejar archivos seleccionados
const handleFileChange = (event: Event, type: "json" | "images") => {
  const input = event.target as HTMLInputElement;
  if (!input.files) return;

  if (type === "json") {
    jsonFile.value = input.files[0]; // Solo un JSON permitido
  } else {
    imageFiles.value = Array.from(input.files); // Varias imágenes
  }
};

// Enviar los archivos al backend
const uploadFiles = () => {
  if (!jsonFile.value) {
    alert("Debes seleccionar un archivo JSON.");
    return;
  }
  if (imageFiles.value.length === 0) {
    alert("Debes seleccionar al menos una imagen.");
    return;
  }

  emit("upload", { json: jsonFile.value, images: imageFiles.value });
  emit("close");
};
</script>

<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
  >
    <div class="bg-gray-900 p-6 rounded-lg shadow-lg w-96">
      <h2 class="text-white text-xl mb-4">Subir Recursos</h2>

      <!-- Subir JSON -->
      <div class="mb-4">
        <label class="text-white">Archivo JSON:</label>
        <input
          type="file"
          accept=".json"
          @change="(e) => handleFileChange(e, 'json')"
          class="w-full text-white"
        />
      </div>

      <!-- Subir Imágenes -->
      <div class="mb-4">
        <label class="text-white">Imágenes:</label>
        <input
          type="file"
          accept="image/*"
          multiple
          @change="(e) => handleFileChange(e, 'images')"
          class="w-full text-white"
        />
      </div>

      <!-- Botones -->
      <div class="flex justify-between mt-4">
        <button
          @click="uploadFiles"
          class="bg-green-500 text-white px-4 py-2 rounded"
        >
          Subir
        </button>
        <button
          @click="$emit('close')"
          class="bg-red-500 text-white px-4 py-2 rounded"
        >
          Cancelar
        </button>
      </div>
    </div>
  </div>
</template>
