<script setup lang="ts">
import { ref, onMounted, nextTick } from "vue";
import { useUserStore } from "../store/userStore"; // Authenticated user
import { createPost } from "../services/postService.ts";
import { getTags } from "../services/taskService.ts";
import { getCategories } from "../services/categoryService.ts";
import { useToast } from "vue-toastification";
import ResourceUploadModal from "../components/resources/ResourceUploadModal.vue";
import "emoji-picker-element";
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

interface Resource {
  id: string;
  title: string;
  description: string;
  tool: string;
}
// Interfaces
interface Category {
  id: string;
  name: string;
}

interface Tag {
  id: string;
  name: string;
}

interface PostForm {
  title: string;
  slug: string;
  content: string;
  category: string;
  tags: Tag[];
  video_url?: string;
  status: "draft" | "published";
  resources: Resource[]; // 🔥 Lista de IDs de recursos en vez de `jsonResource`
  images?: File[];
}

// State
const toast = useToast();
const categories = ref<Category[]>([]);
const tags = ref<Tag[]>([]);
const postForm = ref<PostForm>({
  title: "",
  slug: "",
  content: "",
  category: "",
  tags: [],
  video_url: "",
  status: "draft",
  resources: [], // 🔥 Ahora usamos un array de IDs de recursos
  images: [],
});

const showResourceModal = ref(false);

const handleResourceUpload = (resource: {
  id: string;
  title: string;
  description: string;
  tool: string;
}) => {
  postForm.value.resources.push(resource);
  toast.success(`Recurso "${resource.title}" agregado correctamente. ✅`);
};

const removeResource = (resourceId: string) => {
  postForm.value.resources = postForm.value.resources.filter(
    (resource) => resource.id !== resourceId
  );
  toast.info("Recurso eliminado.");
};

const showEmojiPicker = ref(false);
const emojiPickerRef = ref<HTMLElement | null>(null);
const emojiTarget = ref<"title" | "content" | null>(null);
const imagePreviews = ref<string[]>([]);

// ✅ Open emoji picker above the input
const openEmojiPicker = (field: "title" | "content", event: Event) => {
  emojiTarget.value = field;
  showEmojiPicker.value = true;
  nextTick(() => {
    if (emojiPickerRef.value) {
      const rect = (event.target as HTMLElement).getBoundingClientRect();
      emojiPickerRef.value.style.position = "absolute";
      emojiPickerRef.value.style.top = `${rect.top + window.scrollY - 250}px`;
      emojiPickerRef.value.style.left = `${rect.left + window.scrollX}px`;
      emojiPickerRef.value.style.zIndex = "1000";
    }
  });
};

// ✅ Select emoji
const onEmojiClick = (e: { detail: { unicode: string } }) => {
  if (emojiTarget.value) {
    postForm.value[emojiTarget.value] += e.detail.unicode;
  }
  showEmojiPicker.value = false;
};

// ✅ Fetch categories & tags
const fetchData = async () => {
  categories.value = await getCategories();
  tags.value = await getTags();
};

const submitPost = async () => {
  try {
    const formData = new FormData();
    formData.append("title", postForm.value.title);
    formData.append("slug", postForm.value.slug);
    formData.append("content", postForm.value.content);
    formData.append("category", postForm.value.category);
    formData.append("status", postForm.value.status);

    if (postForm.value.video_url) {
      formData.append("video_url", postForm.value.video_url);
    }

    // ✅ Agregar los tags correctamente
    postForm.value.tags.forEach((tag) => formData.append("tags", tag.id));

    // ✅ Enviar los recursos como objetos completos
    postForm.value.resources.forEach((resource) => {
      formData.append("resources", JSON.stringify(resource)); // 🔥 Convertir el objeto a JSON
    });

    // ✅ Agregar imágenes al FormData
    if (postForm.value.images) {
      postForm.value.images.forEach((image) =>
        formData.append("images", image)
      );
    }

    // ✅ Enviar el post al backend
    await createPost(formData);
    toast.success("Post created successfully! 🎉");

    // ✅ Resetear el formulario después de enviar
    postForm.value = {
      title: "",
      slug: "",
      content: "",
      category: "",
      tags: [],
      video_url: "",
      status: "draft",
      resources: [], // 🔥 Limpiar los recursos guardados
      images: [],
    };
  } catch (error) {
    toast.error("Error creating post. ❌");
  }
};

// ✅ Generate slug automatically
const generateSlug = () => {
  postForm.value.slug = postForm.value.title
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(/[^a-z0-9-]/g, "");
};

// ✅ Handle image uploads & previews
const handleImageUpload = (event: Event) => {
  const files = (event.target as HTMLInputElement).files;
  if (files) {
    for (const file of files) {
      postForm.value.images?.push(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        if (e.target?.result)
          imagePreviews.value.push(e.target.result as string);
      };
      reader.readAsDataURL(file);
    }
  }
};

onMounted(fetchData);
</script>

<template>
  <section class="relative w-full min-h-screen">
    <!-- Background video -->
    <div class="absolute inset-0 w-full min-h-screen h-auto">
      <video
        class="absolute top-0 left-0 w-full h-full min-h-screen object-cover"
        autoplay
        muted
        loop
        playsinline
      >
        <source src="/background4.mp4" type="video/mp4" />
      </video>
    </div>

    <!-- Form container -->
    <div class="relative z-20 w-full px-6 pb-20 pt-12 md:pt-20">
      <div
        class="container mx-auto bg-[#0b1622]/80 backdrop-blur-lg rounded-xl shadow-lg p-6 flex flex-col gap-6"
      >
        <form @submit.prevent="submitPost" class="flex flex-col gap-4">
          <!-- Estructura para diferentes tamaños de pantalla -->
          <div class="grid grid-cols-1 md:grid-cols-12 gap-4">
            <!-- Title -->
            <div class="md:col-span-4">
              <label class="text-white">Title</label>
              <input
                type="text"
                v-model="postForm.title"
                @input="generateSlug"
                @focus="openEmojiPicker('title', $event)"
                class="w-full p-2 rounded bg-gray-800 text-white border border-gray-600"
                required
              />
            </div>

            <!-- Slug -->
            <div class="md:col-span-4">
              <label class="text-white">Slug</label>
              <input
                type="text"
                v-model="postForm.slug"
                class="w-full p-2 rounded bg-gray-800 text-white border border-gray-600"
                readonly
              />
            </div>

            <!-- Category -->
            <div class="md:col-span-3">
              <label class="text-white">Category</label>
              <select
                v-model="postForm.category"
                class="w-full p-2 rounded bg-gray-800 text-white border border-gray-600"
                required
              >
                <option
                  v-for="category in categories"
                  :key="category.id"
                  :value="category.id"
                >
                  {{ category.name }}
                </option>
              </select>
            </div>

            <!-- Status -->
            <div class="md:col-span-1">
              <label class="text-white">Status</label>
              <select
                v-model="postForm.status"
                class="w-full p-2 rounded bg-gray-800 text-white border border-gray-600"
              >
                <option value="draft">Draft</option>
                <option value="published">Published</option>
              </select>
            </div>
          </div>

          <!-- Content -->
          <div>
            <label class="text-white">Content</label>
            <textarea
              v-model="postForm.content"
              @focus="openEmojiPicker('content', $event)"
              class="w-full p-2 rounded bg-gray-800 text-white border border-gray-600"
              rows="5"
            ></textarea>
          </div>

          <!-- Tags -->
          <div class="flex items-center space-x-2">
            <multiselect
              v-model="postForm.tags"
              :options="tags"
              label="name"
              track-by="id"
              multiple
              placeholder="Select your Tags"
              :select-label="'Add'"
              :deselect-label="'Remove'"
              class="tag-selector w-auto min-w-[450px] max-w-full"
            />
          </div>

          <!-- Fila con Video URL, Add JSON y Add Images -->
          <div class="grid grid-cols-1 md:grid-cols-12 gap-4">
            <!-- Video URL -->
            <div class="md:col-span-6">
              <label class="text-white">Video URL</label>
              <input
                type="text"
                v-model="postForm.video_url"
                class="w-full p-2 rounded bg-gray-800 text-white border border-gray-600"
              />
            </div>

            <!-- Botón Add JSON ocupa md:col-span-2 -->
            <div class="md:col-span-2 flex items-end">
              <button
                type="button"
                @click="showResourceModal = true"
                class="w-full bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-700"
              >
                Add JSON
              </button>
            </div>

            <!-- Add Images ocupa md:col-span-2 -->
            <div class="md:col-span-4 flex items-end">
              <input
                type="file"
                multiple
                @change="handleImageUpload"
                class="w-full bg-gray-800 text-white border border-gray-600 p-2 rounded"
                data-button-text="Upload Images"
                data-placeholder="Select files"
              />
            </div>
          </div>

          <!-- 🔥 Nueva fila: Uploaded Resources debajo de la anterior -->
          <div class="grid grid-cols-1 md:grid-cols-12 gap-4 mt-4">
            <div class="md:col-span-12 flex justify-center">
              <div class="grid grid-cols-1 md:grid-cols-6 gap-4 justify-center">
                <div
                  v-for="resource in postForm.resources"
                  :key="resource.id"
                  class="md:col-span-2 bg-white/10 backdrop-blur-2xl border border-white/20 p-3 rounded-xl shadow-lg transition transform hover:scale-105 hover:shadow-xl flex flex-col justify-between h-26"
                >
                  <div>
                    <h3 class="text-base font-bold text-white truncate">
                      {{ resource.title }}
                    </h3>
                    <p
                      class="text-gray-300 text-xs mt-1 truncate"
                      :title="resource.description"
                    >
                      {{ resource.description }}
                    </p>
                    <p class="text-xs text-blue-300">{{ resource.tool }}</p>
                  </div>
                  <div class="flex justify-end mt-0">
                    <button
                      @click="removeResource(resource.id)"
                      class="bg-red-500 text-white px-2 py-1 rounded-lg text-xs hover:bg-red-700 transition"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 📌 Modal para subir recursos -->
          <ResourceUploadModal
            v-if="showResourceModal"
            @upload="handleResourceUpload"
            @close="showResourceModal = false"
          />

          <!-- Submit -->
          <button
            type="submit"
            class="bg-green-500 text-white p-2 rounded-lg hover:bg-green-700"
          >
            🚀 Publish Post
          </button>
        </form>
      </div>
    </div>
  </section>
</template>

<style>
.tag-selector {
  display: inline-block;
  background: transparent !important;
  border: 1px solid white;
  color: white !important;
}

/* ✅ Fondo transparente para el input */
.tag-selector .multiselect__tags {
  background: transparent !important;
  color: white !important;
  border: none !important;
}

/* 📌 Ajusta el tamaño del dropdown en diferentes pantallas */
.multiselect__content-wrapper {
  max-height: 24rem !important;
  width: 100% !important;
  min-width: 350px !important; /* Tamaño mínimo */
  max-width: 600px !important; /* Tamaño máximo */
  overflow: auto !important;
  background-color: black !important;
  color: white !important;
  border: 1px solid white !important;
}

/* ✅ Color de texto blanco en las opciones */
.tag-selector .multiselect__option {
  background-color: black !important;
  color: white !important;
}

/* ✅ Cuando se resalta una opción */
.tag-selector .multiselect__option--highlight {
  background-color: #333 !important;
  color: white !important;
}

/* ✅ Corrige fondo blanco en la selección */
.tag-selector .multiselect__single,
.tag-selector .multiselect__input {
  background: transparent !important;
  color: white !important;
}
</style>
