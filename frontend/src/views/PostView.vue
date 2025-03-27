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
    <div class="relative z-20 w-full px-6">
      <div
        class="container mx-auto bg-[#0b1622]/80 backdrop-blur-lg rounded-xl shadow-lg p-6 flex flex-col gap-6"
      >
        <!-- Filtro de búsqueda -->
        <div class="mt-6">
          <input
            v-model="searchQuery"
            placeholder="Buscar publicaciones..."
            class="w-full px-4 py-2 rounded-lg bg-white/10 text-white placeholder-white/50 border border-white/20"
          />
        </div>

        <!-- Lista de posts -->
        <div class="flex flex-col gap-4">
          <PostCard v-for="post in filteredPosts" :key="post.id" :post="post" />
        </div>
      </div>
    </div>
  </section>
</template>
