<script setup lang="ts">
import { computed } from "vue";
import CategoryCard from "./CategoryCard.vue";

interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string;
  post_count: number;
}

// ✅ Usa tipado directo con defineProps
const props = defineProps<{
  categories: Category[];
}>();

const sortedCategories = computed(() =>
  [...props.categories].sort((a, b) => b.post_count - a.post_count)
);
</script>

<template>
  <div
    class="flex flex-col items-center gap-1 mt-6 mb-20 w-full md:w-3/4 max-w-screen-lg mx-auto"
  >
    <CategoryCard
      v-for="category in sortedCategories"
      :key="category.id"
      :category="category"
    />
  </div>
</template>
