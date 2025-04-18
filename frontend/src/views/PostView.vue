<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import PostCard from "../components/posts/PostCard.vue";
import { getPosts, type Post } from "../services/postService"; // ✅ Usamos la interfaz real

// Estados
const posts = ref<Post[]>([]);
const searchQuery = ref("");

// Fetch
const fetchPosts = async () => {
  const data = await getPosts();
  console.log("📦 Posts recibidos del backend:", data);
  posts.value = data;
};

onMounted(fetchPosts);

// Filtrado por título
const filteredPosts = computed(() =>
  posts.value.filter((post) =>
    post.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
);
</script>

<template>
  <section class="relative w-full min-h-screen">
    <!-- Fondo con video -->
    <div class="absolute inset-0 w-full min-h-screen h-auto">
      <video
        class="absolute top-0 left-0 w-full h-full object-cover"
        autoplay
        muted
        loop
        playsinline
      >
        <source src="/background8.mp4" type="video/mp4" />
        Tu navegador no soporta videos.
      </video>
    </div>

    <!-- Contenido sobre el fondo -->
    <div class="relative z-20 w-full px-2 md:px-16 pt-10 md:pb-10 pb-20">
      <div
        class="container mx-auto bg-[#0b1622]/80 backdrop-blur-lg rounded-xl shadow-lg p-6 flex flex-col gap-6"
      >
        <!-- Filtro de búsqueda con el mismo estilo que CategoryFilter -->
        <div
          class="bg-black/40 backdrop-blur-xl border border-white/30 p-4 rounded-lg shadow-lg flex flex-col sm:flex-row sm:items-center gap-4 mx-auto md:w-3/4"
        >
          <input
            v-model="searchQuery"
            @input="() => {}"
            type="text"
            placeholder="🔎 Search Posts..."
            class="w-full p-3 rounded-md bg-transparent border border-white/40 text-white placeholder-gray-400 focus:outline-none focus:border-blue-400"
          />
        </div>

        <!-- Lista de posts -->
        <div class="flex flex-col items-center gap-4 w-full">
          <PostCard v-for="post in filteredPosts" :key="post.id" :post="post" />
        </div>
      </div>
    </div>
  </section>
</template>
