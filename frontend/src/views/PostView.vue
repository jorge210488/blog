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
  posts.value.filter(
    (post) =>
      post.status === "published" &&
      post.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
);
</script>

<template>
  <section class="relative w-full min-h-screen pb-10 md:pb-6">
    <div class="absolute inset-0 w-full min-h-screen h-auto">
      <div
        class="absolute inset-0 w-full h-full bg-no-repeat bg-top bg-cover"
        style="background-image: url('/fondo1.png')"
      ></div>
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

          <!-- Mensaje si no hay posts -->
          <div
            v-if="filteredPosts.length === 0"
            class="text-white text-center mt-10 space-y-4"
          >
            <p class="text-lg">No posts found.</p>
            <p class="text-lg">Be the first to publish something awesome!</p>

            <router-link
              to="/create-post"
              class="inline-block mt-4 px-5 py-2 border border-white text-white text-lg rounded-lg hover:bg-white hover:text-black transition"
            >
              ✍️ Write Post
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
