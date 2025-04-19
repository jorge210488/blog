<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import PostCard from "../components/posts/PostCard.vue";
import { getUserPosts, type Post } from "../services/postService";

const posts = ref<Post[]>([]);
const searchQuery = ref("");

// Cargar posts del usuario logueado
const fetchMyPosts = async () => {
  posts.value = await getUserPosts();
};

onMounted(fetchMyPosts);

// Filtro por título
const filteredPosts = computed(() =>
  posts.value.filter((post) =>
    post.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
);
</script>

<template>
  <section class="relative w-full min-h-screen">
    <div class="absolute inset-0 w-full min-h-screen h-auto">
      <div
        class="absolute inset-0 w-full h-full bg-repeat-y bg-top bg-contain"
        style="background-image: url('/fondo5.jpg')"
      ></div>
    </div>

    <div class="relative z-20 w-full px-6 md:px-16 pt-10 pb-10">
      <div
        class="container mx-auto bg-[#0b1622]/80 backdrop-blur-lg rounded-xl shadow-lg p-6 flex flex-col gap-6"
      >
        <!-- Filtro -->
        <div
          class="bg-black/40 backdrop-blur-xl border border-white/30 p-4 rounded-lg shadow-lg flex flex-col sm:flex-row sm:items-center gap-4 mx-auto md:w-3/4"
        >
          <input
            v-model="searchQuery"
            type="text"
            placeholder="🔎 Search My Posts..."
            class="w-full p-3 rounded-md bg-transparent border border-white/40 text-white placeholder-gray-400 focus:outline-none focus:border-blue-400"
          />
        </div>

        <!-- Lista -->
        <div class="flex flex-col items-center gap-4 w-full">
          <PostCard v-for="post in filteredPosts" :key="post.id" :post="post" />

          <div
            v-if="filteredPosts.length === 0"
            class="text-white text-center mt-10 space-y-4"
          >
            <p class="text-lg">You haven't published any posts yet.</p>
            <p class="text-lg">Feel free to create your first one!</p>

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
