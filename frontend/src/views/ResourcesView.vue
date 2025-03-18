<script setup lang="ts">
import { ref, onMounted } from "vue";
import ResourceFilter from "../components/resources/ResourceFilter.vue";
import ResourceList from "../components/resources/ResourceList.vue";
import { getResources } from "../services/resourceService.ts";

// Interfaz del recurso
interface Resource {
  id: string;
  title: string;
  description?: string;
  tool: string;
  file: string;
  created_at: string;
  updated_at: string;
}

// Estado para los recursos
const resources = ref<Resource[]>([]);

// Función para obtener recursos
const fetchResources = async () => {
  resources.value = await getResources();
};

// Llamada a la API al montar el componente
onMounted(fetchResources);
</script>

<template>
  <section class="relative w-full min-h-screen">
    <!-- Video de fondo -->
    <video
      class="absolute inset-0 w-full h-full object-cover z-0"
      autoplay
      muted
      loop
      playsinline
    >
      <source src="/background1.mp4" type="video/mp4" />
      Tu navegador no soporta la reproducción de videos.
    </video>

    <!-- Contenedor de los componentes sobre el video -->
    <div
      class="absolute top-32 left-1/2 transform -translate-x-1/2 z-20 w-full px-6"
    >
      <div
        class="container mx-auto bg-[#0b1622]/80 backdrop-blur-lg rounded-xl shadow-lg p-6 flex flex-col gap-6"
      >
        <!-- Asegura que ResourceFilter esté arriba con margen superior -->
        <div class="mt-10">
          <ResourceFilter @filter="fetchResources" />
        </div>

        <ResourceList :resources="resources" />
      </div>
    </div>
  </section>
</template>
