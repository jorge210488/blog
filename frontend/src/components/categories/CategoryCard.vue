<script setup lang="ts">
import type { PropType } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string;
  post_count: number;
}

defineProps({
  category: {
    type: Object as PropType<Category>,
    required: true,
  },
});

const goToCategory = (slug: string) => {
  router.push(`/category/${slug}`);
};
</script>

<template>
  <div
    class="bg-white/20 backdrop-blur-3xl border border-white/40 p-2 rounded-lg shadow-lg w-full sm:w-[80%] md:w-[70%] lg:w-[60%] flex flex-col md:flex-row md:items-center md:justify-between transition transform hover:scale-105 hover:shadow-xl cursor-pointer"
    @click="goToCategory(category.slug)"
  >
    <!-- Primera fila en móviles: Name a la izquierda, Posts a la derecha -->
    <div class="w-full flex justify-between md:hidden">
      <span class="text-white font-bold text-sm">
        {{ category.name }}
      </span>
      <span class="text-blue-400 font-semibold text-sm">
        {{ category.post_count }} posts
      </span>
    </div>

    <!-- Segunda fila en móviles: Descripción centrada -->
    <div v-if="category.description" class="w-full text-center md:hidden">
      <span class="text-gray-300 text-xs">
        {{ category.description }}
      </span>
    </div>

    <!-- Estructura para pantallas estándar en adelante -->
    <div class="hidden md:flex md:w-full md:items-center md:justify-between">
      <!-- Name alineado a la izquierda -->
      <span class="text-white font-bold text-base">
        {{ category.name }}
      </span>

      <!-- Descripción centrada -->
      <div v-if="category.description" class="text-center flex-1">
        <span class="text-gray-300 text-sm">
          {{ category.description }}
        </span>
      </div>

      <!-- Post count alineado a la derecha -->
      <span class="text-blue-400 font-semibold text-base">
        {{ category.post_count }} posts
      </span>
    </div>
  </div>
</template>
