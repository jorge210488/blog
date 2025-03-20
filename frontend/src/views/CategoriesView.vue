<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import CategoryFilter from "../components/categories/CategoriesFilter.vue";
import CategoryList from "../components/categories/CategoriesList.vue";
import { getCategories } from "../services/categoryService";

// Interfaz de la categoría
interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string;
  post_count: number;
}

// Estado de las categorías
const categories = ref<Category[]>([]);
const searchQuery = ref("");

// Función para obtener categorías ordenadas por cantidad de posts
const fetchCategories = async () => {
  categories.value = await getCategories();
};

// Llamada inicial al montar el componente
onMounted(fetchCategories);

// Computed para filtrar las categorías según la búsqueda
const filteredCategories = computed(() => {
  return categories.value.filter((category) =>
    category.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});
</script>

<template>
  <section class="relative w-full min-h-screen">
    <!-- Contenedor del video -->
    <div class="absolute inset-0 w-full min-h-screen h-auto">
      <video
        class="absolute top-0 left-0 w-full h-full min-h-screen object-cover"
        autoplay
        muted
        loop
        playsinline
      >
        <source src="/background8.mp4" type="video/mp4" />
        Tu navegador no soporta la reproducción de videos.
      </video>
    </div>

    <!-- Contenedor de los componentes sobre el video -->
    <div class="relative z-20 w-full px-6">
      <div
        class="container mx-auto bg-[#0b1622]/80 backdrop-blur-lg rounded-xl shadow-lg p-6 flex flex-col gap-6"
      >
        <!-- Filtros -->
        <div class="mt-10">
          <CategoryFilter @filter="searchQuery = $event" />
        </div>

        <!-- Lista de Categorías -->
        <CategoryList :categories="filteredCategories" />
      </div>
    </div>
  </section>
</template>
