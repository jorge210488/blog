<script setup lang="ts">
import { ref } from "vue";
import ResourcesModal from "./ResourcesModal.vue";
import { useUserStore } from "../../store/userStore";
import { computed } from "vue";
import { deletePost } from "../../services/postService"; // ajusta la ruta si es necesario
import { useRouter } from "vue-router";

const router = useRouter();

const props = defineProps<{
  post: {
    id: string;
    title: string;
    slug: string;
    content: string;
    author: string;
    category: {
      id: string;
      name: string;
      slug: string;
      description?: string;
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
      description?: string;
      file: string;
      tool?: string;
      created_at?: string;
      updated_at?: string;
    }[];
    video_url?: string;
    views: number;
    status: string;
    created_at: string;
    updated_at: string;
  };
}>();

const userStore = useUserStore();
const isAuthor = computed(() => userStore.user?.email === props.post.author);

const showImageModal = ref(false);
const selectedImage = ref("");

const openImage = (url: string) => {
  selectedImage.value = url;
  showImageModal.value = true;
};

const closeImage = () => {
  showImageModal.value = false;
};

const showResourcesModal = ref(false);
const openResources = () => {
  showResourcesModal.value = true;
};
const closeResources = () => {
  showResourcesModal.value = false;
};

const handleDelete = async () => {
  const confirmed = window.confirm(
    "¿Estás seguro de que deseas eliminar este post?"
  );
  if (!confirmed) return;

  const success = await deletePost(props.post.id);
  if (success) {
    alert("✅ Post deleted successfully");
    router.push("/my-posts");
  } else {
    alert("❌ An error occurred while deleting the post");
  }
};
</script>

<template>
  <div
    class="w-full max-w-[800px] h-[520px] mx-auto bg-[#172a3a] border border-white/10 rounded-xl shadow-md px-6 py-4 flex flex-col justify-between text-white"
  >
    <!-- Contenido -->
    <div class="flex flex-col justify-between h-full">
      <div class="flex flex-col gap-3">
        <!-- Cabecera -->
        <div class="flex justify-between items-center">
          <h2 class="text-2xl font-bold">{{ post.title }}</h2>
          <div class="text-xs text-white/60">
            {{ new Date(post.created_at).toLocaleDateString() }}
          </div>
        </div>

        <!-- Autor, categoría, vistas -->
        <div class="text-sm text-white/70 flex flex-wrap gap-3">
          <span>👤 {{ post.author }}</span>
          <span v-if="post.category">🏷️ {{ post.category.name }}</span>
          <span>👁️ {{ post.views }} vistas</span>
        </div>

        <!-- Contenido -->
        <p class="text-base leading-relaxed line-clamp-3">
          {{ post.content }}
        </p>

        <!-- Tags -->
        <div v-if="post.tags?.length" class="flex gap-2 flex-wrap">
          <span
            v-for="tag in post.tags"
            :key="tag.id"
            class="px-3 py-1 text-xs rounded-full bg-white/10 border border-white/20"
          >
            #{{ tag.name }}
          </span>
        </div>
        <!-- Imágenes -->
        <div class="mt-2 min-h-[64px]">
          <!-- MOBILE (pantallas menores a md) -->
          <div
            v-if="post.images?.length"
            class="block md:hidden overflow-x-auto whitespace-nowrap"
          >
            <div
              v-for="image in post.images"
              :key="image.id"
              class="inline-block align-top w-12 h-12 bg-white/10 border border-white/10 rounded mr-2 cursor-pointer"
              @click="openImage(image.image_url)"
            >
              <img
                :src="image.image_url"
                alt="Imagen"
                class="w-full h-full object-contain block"
              />
            </div>
          </div>

          <!-- DESKTOP -->
          <div
            v-if="post.images?.length"
            class="hidden md:grid grid-cols-6 gap-2"
          >
            <div
              v-for="image in post.images"
              :key="image.id"
              class="w-full h-[64px] bg-white/10 border border-white/10 rounded overflow-hidden cursor-pointer"
              @click="openImage(image.image_url)"
            >
              <img
                :src="image.image_url"
                alt="Imagen"
                class="w-full h-full object-contain block"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Botones -->
      <div class="mt-4 flex gap-0 md:gap-6">
        <button
          class="bg-white/10 px-2 md:px-4 py-2 rounded-lg text-sm hover:bg-white/20 transition"
        >
          💬 Comment
        </button>
        <button
          class="bg-white/10 px-4 py-2 rounded-lg text-sm hover:bg-white/20 transition"
        >
          👍 Like
        </button>
        <button
          class="bg-white/10 px-4 py-2 rounded-lg text-sm hover:bg-white/20 transition"
        >
          🔗 Share
        </button>
        <!-- Botón para abrir modal de recursos -->
        <button
          v-if="Array.isArray(post.resources) && post.resources.length"
          @click="openResources"
          class="mt-2 px-4 py-2 bg-white/10 text-sm rounded hover:bg-white/20 transition"
        >
          📎 Resources
        </button>
      </div>
      <div v-if="isAuthor" class="flex gap-4 justify-center md:justify-end">
        <button
          class="px-4 py-2 border border-white rounded-lg hover:bg-white hover:text-black transition text-sm"
        >
          ✏️ Edit
        </button>
        <button
          @click="handleDelete"
          class="px-4 py-2 border border-white rounded-lg hover:bg-white hover:text-black transition text-sm"
        >
          🗑️ Delete
        </button>
      </div>
    </div>

    <!-- Modal -->
    <div
      v-if="showImageModal"
      class="fixed inset-0 bg-black/80 flex items-center justify-center z-50"
      @click.self="closeImage"
      @keyup.esc="closeImage"
      tabindex="0"
    >
      <img
        :src="selectedImage"
        class="max-w-full max-h-full rounded-xl"
        alt="Imagen ampliada"
      />
    </div>
  </div>

  <ResourcesModal
    :show="showResourcesModal"
    :resources="post.resources || []"
    @close="closeResources"
  />
</template>
