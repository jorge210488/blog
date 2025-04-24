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
  const allPosts = await getPosts({ category: categorySlug.value });
  posts.value = allPosts.filter((post) => post.status === "published");
};

onMounted(fetchPostsByCategory);
</script>

<template>
  <section class="relative w-full min-h-screen pb-10 md:pb-6">
    <div class="absolute inset-0 w-full min-h-screen h-auto">
      <div
        class="absolute inset-0 w-full h-full bg-no-repeat bg-top bg-cover"
        style="background-image: url('/fondo1.png')"
      ></div>
    </div>

    <!-- Contenido -->
    <div
      class="relative z-20 w-full px-6 md:px-16 py-10 container mx-auto bg-[#0b1622]/80 backdrop-blur-lg rounded-xl shadow-lg"
    >
      <h1 class="text-2xl font-bold text-white mb-6 mt-6">
        Posts in Category "{{ categorySlug }}"
      </h1>

      <!-- Lista de posts -->
      <div v-if="posts.length" class="grid gap-6">
        <PostCard v-for="post in posts" :key="post.id" :post="post" />
      </div>

      <!-- Mensaje si no hay posts, sin borde ni fondo extra -->
      <div v-else class="text-white text-center mt-10 space-y-4">
        <p class="text-lg">No posts found in this category.</p>
        <p class="text-lg">Be the first to publish something awesome!</p>

        <router-link
          to="/create-post"
          class="inline-block mt-4 px-5 py-2 border border-white text-white text-lg rounded-lg hover:bg-white hover:text-black transition"
        >
          ✍️ Write Post
        </router-link>
      </div>
    </div>
  </section>
</template>
