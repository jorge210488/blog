<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { getPosts } from "../services/postService";
import PostCard from "../components/posts/PostCard.vue";
import type { Post } from "../services/postService";

const route = useRoute();
const posts = ref<Post[]>([]);
const categorySlug = ref(route.params.slug as string);

const fetchPostsByCategory = async () => {
  posts.value = await getPosts({ category: categorySlug.value });
};

onMounted(fetchPostsByCategory);
</script>

<template>
  <section class="relative w-full min-h-screen">
    <!-- Fondo -->
    <div class="absolute inset-0 w-full h-full">
      <video
        class="absolute top-0 left-0 w-full h-full object-cover"
        autoplay
        muted
        loop
        playsinline
      >
        <source src="/background8.mp4" type="video/mp4" />
      </video>
    </div>

    <!-- Contenido -->
    <div
      class="relative z-20 w-full px-6 py-10 container mx-auto bg-[#0b1622]/80 backdrop-blur-lg rounded-xl shadow-lg"
    >
      <h1 class="text-2xl font-bold text-white mb-6 mt-6">
        Posts in Category "{{ categorySlug }}"
      </h1>

      <div v-if="posts.length" class="grid gap-6">
        <PostCard v-for="post in posts" :key="post.id" :post="post" />
      </div>
      <p v-else class="text-white/70 text-center mt-4">No Post Available.</p>
    </div>
  </section>
</template>
