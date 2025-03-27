<script setup lang="ts">
defineProps<{
  post: {
    id: string;
    title: string;
    slug: string;
    content: string;
    author: string;
    category: {
      id: string;
      name: string;
    };
    tags: {
      id: string;
      name: string;
    }[];
    images: {
      id: string;
      image_url: string;
    }[];
    resources: {
      id: string;
      title: string;
      file: string;
    }[];
    video_url?: string;
    views: number;
    status: string;
    created_at: string;
    updated_at: string;
  };
}>();
</script>

<template>
  <div
    class="w-full bg-[#172a3a] border border-white/10 rounded-xl shadow-md p-4 flex gap-4 items-start"
  >
    <!-- Imagen -->
    <div
      v-if="post.images.length > 0"
      class="w-28 h-28 rounded overflow-hidden flex-shrink-0"
    >
      <img
        :src="post.images[0].image_url"
        alt="Post Image"
        class="object-cover w-full h-full"
      />
    </div>

    <!-- Contenido -->
    <div class="flex-1">
      <h2 class="text-white text-lg font-semibold">{{ post.title }}</h2>
      <p class="text-white/70 text-sm line-clamp-3">{{ post.content }}</p>

      <div class="text-xs text-white/50 mt-2 flex gap-2 flex-wrap">
        <span>{{ post.author }}</span>
        <span>• {{ new Date(post.created_at).toLocaleDateString() }}</span>
        <span>• {{ post.views }} vistas</span>
        <span>• {{ post.category.name }}</span>
      </div>

      <!-- Tags -->
      <div class="mt-2 flex gap-1 flex-wrap">
        <span
          v-for="tag in post.tags"
          :key="tag.id"
          class="px-2 py-0.5 text-xs rounded-full bg-white/10 text-white border border-white/20"
        >
          #{{ tag.name }}
        </span>
      </div>

      <!-- Recursos -->
      <div v-if="post.resources.length" class="mt-3">
        <p class="text-white/70 text-sm mb-1">Recursos:</p>
        <ul class="list-disc list-inside text-white/90 text-sm">
          <li v-for="resource in post.resources" :key="resource.id">
            <a
              :href="resource.file"
              target="_blank"
              class="underline hover:text-white"
            >
              {{ resource.title }}
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
