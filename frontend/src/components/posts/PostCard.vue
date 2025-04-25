<script setup lang="ts">
import { onMounted, ref } from "vue";
import ResourcesModal from "./ResourcesModal.vue";
import { useUserStore } from "../../store/userStore";
import { computed } from "vue";
import { deletePost, countPostView } from "../../services/postService";
import { useRouter } from "vue-router";
import UpdatePostModal from "./UpdatePostModal.vue";
import CommentsModal from "../comments/CommentsModal.vue";
import {
  getLikesByPost,
  likePost,
  unlikePost,
  type Like,
} from "../../services/likeService";

const likes = ref<Like[]>([]);
const liked = ref(false);
const likeId = ref<string | null>(null);
const likeCount = computed(() => likes.value.length);
const showCommentsModal = ref(false);

const fetchLikes = async () => {
  const result = await getLikesByPost(props.post.id);
  likes.value = result;

  const match = result.find((like) => like.user === userStore.user?.id);
  if (match) {
    liked.value = true;
    likeId.value = match.id;
  }
};

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

const getEmbedUrl = (video_url?: string) => {
  if (!video_url) return "";

  try {
    // Si es una URL completa con v= param
    const url = new URL(video_url);
    const videoId = url.searchParams.get("v");
    if (videoId) return `https://www.youtube.com/embed/${videoId}`;
  } catch {
    // Si es un link acortado tipo youtu.be/nmz7cyvj7Zc
    const match = video_url.match(/youtu\.be\/([^\?&]+)/);
    if (match) return `https://www.youtube.com/embed/${match[1]}`;
  }

  return "";
};

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

const showEditModal = ref(false);
const openEditModal = () => {
  showEditModal.value = true;
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

const postElement = ref<HTMLElement | null>(null);
const hasCountedView = ref(false);

onMounted(() => {
  fetchLikes();

  const observer = new IntersectionObserver(
    async ([entry]) => {
      if (entry.isIntersecting && !hasCountedView.value) {
        hasCountedView.value = true; // solo una vez
        const newViewCount = await countPostView(props.post.id);
        if (newViewCount !== null) {
          props.post.views = newViewCount;
        }
        observer.disconnect(); // deja de observar
      }
    },
    { threshold: 0.5 } // 50% visible
  );

  if (postElement.value) {
    observer.observe(postElement.value);
  }
});

const handleLikeClick = async () => {
  if (!userStore.user) {
    alert("You must be logged in to like posts.");
    return;
  }

  if (liked.value && likeId.value) {
    const oldLikeId = likeId.value; // ✅ Guarda antes de limpiar

    const success = await unlikePost(oldLikeId);
    if (success) {
      liked.value = false;
      likeId.value = null;
      likes.value = likes.value.filter((like) => like.id !== oldLikeId); // ✅ Filtra correctamente
    }
  } else {
    const newLike = await likePost(props.post.id);
    if (newLike) {
      liked.value = true;
      likeId.value = newLike.id;
      likes.value.push(newLike);
    }
  }
};

const handleClickResources = () => {
  if (!userStore.user) {
    window.alert("You must be logged in to access resources.");
    return;
  }
  openResources();
};

const handleClickComments = () => {
  if (!userStore.user) {
    window.alert("You must be logged in to comment.");
    return;
  }
  showCommentsModal.value = true;
};

const handleShare = async () => {
  const baseUrl = import.meta.env.VITE_FRONTEND_URL || window.location.origin;
  const fullUrl = `${baseUrl.replace(/\/$/, "")}/posts/${props.post.slug}`;

  try {
    await navigator.clipboard.writeText(fullUrl);
    alert("🔗 Link copied to clipboard!");
  } catch (err) {
    console.error("❌ Failed to copy:", err);
    alert("❌ Could not copy the link");
  }
};
</script>

<template>
  <div
    ref="postElement"
    class="w-full max-w-[800px] min-h-[520px] mx-auto bg-[#172a3a] border border-white/10 rounded-xl shadow-md px-6 py-4 flex flex-col justify-between text-white"
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

        <!-- Info principal en columnas -->
        <div class="flex flex-col md:flex-row gap-6">
          <!-- Columna izquierda -->
          <div class="flex-1 flex flex-col gap-4">
            <!-- Fila 1: autor, categoría, vistas -->
            <div class="text-sm text-white/70 flex flex-wrap gap-3">
              <span>👤 {{ post.author }}</span>
              <span v-if="post.category">🏷️ {{ post.category.name }}</span>
              <span>👁️ {{ post.views }} views</span>
            </div>

            <!-- Fila 2: contenido -->
            <p class="text-sm md:text-base leading-relaxed whitespace-pre-line">
              {{ post.content }}
            </p>

            <!-- Fila 3: tags -->
            <div v-if="post.tags?.length" class="flex gap-2 flex-wrap">
              <span
                v-for="tag in post.tags"
                :key="tag.id"
                class="px-3 py-1 text-xs rounded-full bg-white/10 border border-white/20"
              >
                #{{ tag.name }}
              </span>
            </div>
          </div>

          <!-- Columna derecha: video -->

          <!-- Versión para pantallas pequeñas -->
          <div
            v-if="post.video_url"
            class="block md:hidden mt-4 flex justify-center items-start"
          >
            <div
              class="w-full max-w-[600px] aspect-[16/9] rounded-lg overflow-hidden border border-white/20"
            >
              <iframe
                class="w-full h-full"
                :src="getEmbedUrl(post.video_url)"
                title="YouTube video"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowfullscreen
              ></iframe>
            </div>
          </div>

          <!-- Versión para pantallas md y mayores -->
          <div
            v-if="post.video_url"
            class="hidden md:flex mt-0 md:pr-20 justify-center items-start"
          >
            <div
              style="width: 500px; height: 285px"
              class="rounded-lg overflow-hidden border border-white/20"
            >
              <iframe
                width="500"
                height="285"
                :src="getEmbedUrl(post.video_url)"
                title="YouTube video"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowfullscreen
              ></iframe>
            </div>
          </div>
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
            class="hidden md:grid grid-cols-8 gap-2"
          >
            <div
              v-for="image in post.images"
              :key="image.id"
              class="w-full h-[32px] bg-white/10 border border-white/10 rounded overflow-hidden cursor-pointer"
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
      <div class="mt-4 flex flex-wrap items-center gap-2 md:gap-4">
        <!-- Left-side buttons -->
        <button
          @click="handleClickComments"
          class="bg-white/10 px-2 md:px-4 py-2 rounded-lg text-sm hover:bg-white/20 transition"
        >
          💬 Comment
        </button>

        <button
          @click="handleLikeClick"
          class="bg-white/10 px-4 py-2 rounded-lg text-sm hover:bg-white/20 transition"
        >
          {{ liked ? "❤️ Liked" : "🤍 Like" }} ({{ likeCount }})
        </button>
        <button
          @click="handleShare"
          class="bg-white/10 px-4 py-2 rounded-lg text-sm hover:bg-white/20 transition"
        >
          🔗 Share
        </button>
        <button
          v-if="Array.isArray(post.resources) && post.resources.length"
          @click="handleClickResources"
          class="px-4 py-2 bg-white/10 text-sm rounded hover:bg-white/20 transition"
        >
          📎 Resources
        </button>

        <!-- Right-side (author only) -->
        <template v-if="isAuthor">
          <div class="ml-auto flex gap-2">
            <span
              v-if="post.status === 'draft'"
              class="text-sm italic bg-pink-300 px-4 py-2 rounded-lg"
            >
              Draft
            </span>
            <button
              @click="openEditModal"
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
        </template>
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
  <UpdatePostModal
    v-if="showEditModal"
    :show="showEditModal"
    :post="post"
    @close="showEditModal = false"
  />
  <CommentsModal
    :post-id="post.id"
    :show="showCommentsModal"
    @close="showCommentsModal = false"
  />
</template>
