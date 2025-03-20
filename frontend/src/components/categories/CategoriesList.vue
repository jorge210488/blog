<script setup lang="ts">
import CategoryCard from "./CategoryCard.vue";
import type { PropType } from "vue";

interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string;
  post_count: number;
}

defineProps({
  categories: {
    type: Array as PropType<Category[]>,
    required: true,
  },
});
</script>

<template>
  <div
    class="flex flex-col items-center gap-1 mt-6 mb-20 w-full md:w-3/4 max-w-screen-lg mx-auto"
  >
    <CategoryCard
      v-for="category in categories"
      :key="category.id"
      :category="category"
    />
  </div>
</template>
