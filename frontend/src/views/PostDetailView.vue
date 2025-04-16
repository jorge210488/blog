<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { getPostBySlug } from "../services/postService";
import type { Post } from "../services/postService";
import PostCard from "../components/posts/PostCard.vue";

const route = useRoute();
const slug = route.params.slug as string;

const post = ref<Post | null>(null);
const loading = ref(true);

onMounted(async () => {
  post.value = await getPostBySlug(slug);
  loading.value = false;
});
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
    <div class="relative z-20 w-full px-6 pt-10">
      <div
        class="container mx-auto bg-[#0b1622]/80 backdrop-blur-lg rounded-xl shadow-lg p-6 flex flex-col gap-6"
      >
        <div v-if="loading" class="text-center text-white/70 text-sm">
          Cargando post...
        </div>
        <div v-else-if="post">
          <PostCard :post="post" />
        </div>
        <div v-else class="text-center text-red-400 text-sm">
          Post no encontrado.
        </div>
      </div>
    </div>
  </section>
</template>
