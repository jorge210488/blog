<script setup lang="ts">
import { ref, onMounted, nextTick } from "vue";
import { useUserStore } from "../store/userStore"; // Authenticated user
import { createPost } from "../services/postService.ts";
import { getTags } from "../services/taskService.ts";
import { getCategories } from "../services/categoryService.ts";
import { useToast } from "vue-toastification";
import ResourceUploadModal from "../components/resources/ResourceUploadModal.vue";
import "emoji-picker-element";

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
  tags: string[];
  video_url?: string;
  status: "draft" | "published";
  jsonResource?: File | null;
  images?: File[];
}

// State
const toast = useToast();
const userStore = useUserStore();
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
  jsonResource: null,
  images: [],
});
const showResourceModal = ref(false);
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

// ✅ Submit form
const submitPost = async () => {
  try {
    const formData = new FormData();
    formData.append("title", postForm.value.title);
    formData.append("slug", postForm.value.slug);
    formData.append("content", postForm.value.content);
    formData.append("category", postForm.value.category);
    formData.append("status", postForm.value.status);
    if (postForm.value.video_url)
      formData.append("video_url", postForm.value.video_url);
    postForm.value.tags.forEach((tag) => formData.append("tags", tag));

    if (postForm.value.jsonResource) {
      formData.append("resource", postForm.value.jsonResource);
    }

    if (postForm.value.images) {
      postForm.value.images.forEach((image) =>
        formData.append("images", image)
      );
    }

    await createPost(formData);
    toast.success("Post created successfully! 🎉");

    // Reset form
    postForm.value = {
      title: "",
      slug: "",
      content: "",
      category: "",
      tags: [],
      video_url: "",
      status: "draft",
      jsonResource: null,
      images: [],
    };
    imagePreviews.value = [];
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

// ✅ Capture files from modal
const handleUpload = ({
  json,
  images,
}: {
  json: File | null;
  images: File[];
}) => {
  postForm.value.jsonResource = json;
  postForm.value.images = images;
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
    <div class="relative z-20 w-full px-6">
      <div
        class="container mx-auto bg-[#0b1622]/80 backdrop-blur-lg rounded-xl shadow-lg p-6 flex flex-col gap-6"
      >
        <h2 class="text-white text-2xl font-semibold">Create New Post</h2>

        <form @submit.prevent="submitPost" class="flex flex-col gap-4">
          <!-- Title -->
          <div>
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

          <!-- Slug, Category, Status (Same Row) -->
          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="text-white">Slug</label>
              <input
                type="text"
                v-model="postForm.slug"
                class="w-full p-2 rounded bg-gray-800 text-white border border-gray-600"
                readonly
              />
            </div>

            <div>
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

            <div>
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
          <div>
            <label class="text-white">Tags</label>
            <v-select
              v-model="postForm.tags"
              :options="tags"
              label="name"
              multiple
              class="bg-gray-800 text-white"
            />
          </div>

          <!-- Add Resources & Add Images -->
          <button
            type="button"
            @click="showResourceModal = true"
            class="bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-700"
          >
            📎 Add Resources
          </button>
          <input
            type="file"
            multiple
            @change="handleImageUpload"
            class="bg-gray-800 text-white border border-gray-600 p-2 rounded"
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
