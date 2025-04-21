<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { getPostsByCategory } from "../services/postService.ts";
import ResourceList from "../components/resources/ResourceList.vue";
import type { Resource } from "../services/resourceService";

// Definir la estructura de un post
interface Post {
  id: string;
  title: string;
  slug: string;
  content: string;
  created_at: string;
  updated_at: string;
  resources: Resource[];
}

const route = useRoute();
const categorySlug = ref<string>(route.params.slug as string);
const posts = ref<Post[]>([]);

// Obtener los posts de la categoría
const fetchPosts = async () => {
  posts.value = await getPostsByCategory(categorySlug.value);
};

onMounted(fetchPosts);
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
        <source src="/background4.mp4" type="video/mp4" />
        Tu navegador no soporta la reproducción de videos.
      </video>
    </div>

    <!-- Contenedor de los posts -->
    <div class="relative z-20 w-full px-6">
      <div
        class="container mx-auto bg-[#0b1622]/80 backdrop-blur-lg rounded-xl shadow-lg p-6 flex flex-col gap-6"
      >
        <h2 class="text-3xl font-bold text-white">
          Posts in {{ categorySlug }}
        </h2>

        <!-- Lista de Posts -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
          <div
            v-for="post in posts"
            :key="post.id"
            class="bg-white/10 backdrop-blur-2xl border border-white/20 p-6 rounded-xl shadow-lg transition transform hover:scale-105 hover:shadow-xl"
          >
            <h3 class="text-xl font-bold text-white">{{ post.title }}</h3>
            <p class="text-gray-300 text-sm mt-2">
              {{ post.content.substring(0, 100) }}...
            </p>
            <a
              :href="'/post/' + post.slug"
              class="text-blue-400 mt-4 font-semibold"
            >
              Read more
            </a>

            <!-- Recursos del Post -->
            <ResourceList
              v-if="post.resources.length"
              :resources="post.resources"
            />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
