<script setup lang="ts">
import { ref, onMounted } from "vue";
import ResourceFilter from "../components/resources/ResourceFilter.vue";
import ResourceList from "../components/resources/ResourceList.vue";
import { getResources } from "../services/resourceService.ts";
import type { Resource, ResourceFilters } from "../services/resourceService";
import { useUserStore } from "../store/userStore";
import { computed } from "vue";

// Estado de los recursos
const resources = ref<Resource[]>([]);
const userStore = useUserStore();

// Estado de los filtros, asegurando que `sortBy` sea del tipo correcto
const filterOptions = ref<ResourceFilters>({
  search: "",
  tool: "",
  sortBy: "-updated_at", // Aseguramos el tipo correcto
});

// Función para obtener recursos con filtros
const fetchResources = async (
  filters: ResourceFilters = filterOptions.value
) => {
  filterOptions.value = {
    ...filters,
    sortBy: filters.sortBy ?? "-updated_at", // Asegurar el valor por defecto
  };
  resources.value = await getResources(filterOptions.value);
};

const filteredResources = computed(() => {
  // Si está filtrando por el usuario actual
  if (filterOptions.value.owner === "me" && userStore.user) {
    return resources.value.filter(
      (resource) => resource.user_id === userStore.user?.id
    );
  }

  // Mostrar todos los recursos
  return resources.value;
});

// Llamada inicial al montar el componente
onMounted(fetchResources);
</script>

<template>
  <section class="relative w-full min-h-screen">
    <!-- Contenedor del video -->
    <div class="absolute inset-0 w-full min-h-screen h-auto">
      <video
        class="pointer-events-none absolute top-0 left-0 w-full h-full min-h-screen object-cover"
        autoplay
        muted
        loop
        playsinline
      >
        <source src="/background4.mp4" type="video/mp4" />
        Tu navegador no soporta la reproducción de videos.
      </video>

      <!-- Duplicación del video en pantallas pequeñas -->
      <video
        class="absolute top-0 left-0 w-full h-full min-h-screen object-cover sm:hidden"
        autoplay
        muted
        loop
        playsinline
      >
        <source src="/background4.mp4" type="video/mp4" />
      </video>
    </div>

    <!-- Contenedor de los componentes sobre el video -->
    <div class="relative w-full px-6">
      <div
        class="container mx-auto bg-[#0b1622]/80 backdrop-blur-lg rounded-xl shadow-lg p-6 flex flex-col gap-6"
      >
        <!-- Filtros -->
        <div class="mt-10">
          <ResourceFilter @filter="fetchResources" />
        </div>

        <!-- Lista de Recursos -->
        <ResourceList :resources="filteredResources" />
      </div>
    </div>
  </section>
</template>
