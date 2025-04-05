<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from "vue";
import { useToast } from "vue-toastification";
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";
import "emoji-picker-element";
import { getCategories } from "../../services/categoryService";
import { getTags } from "../../services/taskService";
import { updatePost } from "../../services/postService";
import ResourceUploadModal from "../resources/ResourceUploadModal.vue";
import ResourceSelectionModal from "../resources/ResourceSelectionModal.vue";

interface Resource {
  id: string;
  title: string;
  description: string;
  tool: string;
}

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
  resources: string[];
  resourcesDetails: Resource[];
  images?: File[];
}

const props = defineProps<{
  show: boolean;
  post: any;
}>();
const emit = defineEmits(["close", "updated"]);

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
  resources: [],
  resourcesDetails: [],
  images: [],
});

const imagePreviews = ref<string[]>([]);
const showResourceModal = ref(false);
const showResourceSelectionModal = ref(false);
const showEmojiPicker = ref(false);
const emojiTarget = ref<"title" | "content" | null>(null);
const emojiPickerRef = ref<HTMLElement | null>(null);

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

const onEmojiClick = (e: { detail: { unicode: string } }) => {
  if (emojiTarget.value) {
    postForm.value[emojiTarget.value] += e.detail.unicode;
  }
  showEmojiPicker.value = false;
};

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

const handleResourceUpload = (resource: Resource) => {
  postForm.value.resources.push(resource.id);
  postForm.value.resourcesDetails.push(resource);
  toast.success(`Resource "${resource.title}" added successfully.`);
};

const handleSelectedResources = (selectedResources: Resource[]) => {
  selectedResources.forEach((resource) => {
    if (!postForm.value.resources.includes(resource.id)) {
      postForm.value.resources.push(resource.id);
      postForm.value.resourcesDetails.push(resource);
    }
  });
};

const removeResource = (resourceId: string) => {
  postForm.value.resources = postForm.value.resources.filter(
    (id) => id !== resourceId
  );
  postForm.value.resourcesDetails = postForm.value.resourcesDetails.filter(
    (r) => r.id !== resourceId
  );
  toast.info("Resource removed.");
};

const generateSlug = () => {
  postForm.value.slug = postForm.value.title
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(/[^a-z0-9-]/g, "");
};

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
    postForm.value.tags.forEach((tag) => formData.append("tags", tag.id));
    postForm.value.resources.forEach((id) => formData.append("resources", id));
    postForm.value.images?.forEach((img) => formData.append("images", img));

    await updatePost(props.post.id, formData);
    toast.success("Post updated successfully!");
    emit("updated");
    emit("close");
  } catch (error) {
    toast.error("Error updating post.");
  }
};

const initForm = async () => {
  const p = props.post;
  postForm.value = {
    title: p.title,
    slug: p.slug,
    content: p.content,
    category: p.category.id,
    tags: p.tags,
    video_url: p.video_url || "",
    status: p.status,
    resources: p.resources.map((r: any) => r.id),
    resourcesDetails: p.resources,
    images: [],
  };
};

onMounted(async () => {
  await fetchData();
  initForm();
});

watch(() => props.post, initForm);

const fetchData = async () => {
  categories.value = await getCategories();
  tags.value = await getTags();
};
</script>

<template>
  <div
    class="fixed inset-0 z-[9999] bg-black bg-opacity-90 backdrop-blur-sm flex items-center justify-center px-4 overflow-y-auto"
    @click.self="emit('close')"
  >
    <div
      class="relative w-full max-w-6xl bg-[#0b1622]/90 backdrop-blur-lg rounded-xl shadow-lg p-6 flex flex-col gap-6 mt-20 mb-10"
    >
      <button
        @click="$emit('close')"
        class="absolute top-4 right-4 text-white hover:text-red-500 text-xl"
      >
        ✖
      </button>

      <!-- Formulario completo integrado para actualización -->
      <section class="relative w-full">
        <div class="relative z-20 w-full">
          <div
            class="bg-[#0b1622]/80 backdrop-blur-lg rounded-xl shadow-lg p-6 flex flex-col gap-6"
          >
            <form @submit.prevent="submitPost" class="flex flex-col gap-4">
              <!-- Campos idénticos al formulario de creación -->
              <div class="grid grid-cols-1 md:grid-cols-12 gap-4">
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
                <div class="md:col-span-4">
                  <label class="text-white">Slug</label>
                  <input
                    type="text"
                    v-model="postForm.slug"
                    class="w-full p-2 rounded bg-gray-800 text-white border border-gray-600"
                    readonly
                  />
                </div>
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
              <div>
                <label class="text-white">Content</label>
                <textarea
                  v-model="postForm.content"
                  @focus="openEmojiPicker('content', $event)"
                  class="w-full p-2 rounded bg-gray-800 text-white border border-gray-600"
                  rows="5"
                ></textarea>
              </div>
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
              <div class="grid grid-cols-1 md:grid-cols-12 gap-4">
                <div class="md:col-span-4">
                  <label class="text-white">Video URL</label>
                  <input
                    type="text"
                    v-model="postForm.video_url"
                    class="w-full p-2 rounded bg-gray-800 text-white border border-gray-600"
                  />
                </div>
                <div class="md:col-span-2 flex items-end">
                  <button
                    type="button"
                    @click="showResourceModal = true"
                    class="w-full bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-700"
                  >
                    Add Resource
                  </button>
                </div>
                <div class="md:col-span-2 flex items-end">
                  <button
                    type="button"
                    @click="showResourceSelectionModal = true"
                    class="w-full bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-700"
                  >
                    Choose Resources
                  </button>
                </div>
                <div class="md:col-span-4 flex items-end">
                  <input
                    type="file"
                    multiple
                    @change="handleImageUpload"
                    class="w-full bg-gray-800 text-white border border-gray-600 p-2 rounded"
                  />
                </div>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-12 gap-4 mt-4">
                <div class="md:col-span-12 flex justify-center">
                  <div
                    class="grid grid-cols-1 md:grid-cols-6 gap-4 justify-center"
                  >
                    <div
                      v-for="resource in postForm.resourcesDetails"
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
              <ResourceUploadModal
                v-if="showResourceModal"
                @upload="handleResourceUpload"
                @close="showResourceModal = false"
              />
              <ResourceSelectionModal
                v-if="showResourceSelectionModal"
                @close="showResourceSelectionModal = false"
                @addResources="handleSelectedResources"
              />
              <button
                type="submit"
                class="bg-yellow-500 text-white p-2 rounded-lg hover:bg-yellow-600"
              >
                💾 Update Post
              </button>
            </form>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style>
@import "vue-multiselect/dist/vue-multiselect.css";
.tag-selector {
  display: inline-block;
  background: transparent !important;
  border: 1px solid white;
  color: white !important;
}
.tag-selector .multiselect__tags {
  background: transparent !important;
  color: white !important;
  border: none !important;
}
.multiselect__content-wrapper {
  max-height: 24rem !important;
  width: 100% !important;
  min-width: 350px !important;
  max-width: 600px !important;
  overflow: auto !important;
  background-color: black !important;
  color: white !important;
  border: 1px solid white !important;
}
.tag-selector .multiselect__option {
  background-color: black !important;
  color: white !important;
}
.tag-selector .multiselect__option--highlight {
  background-color: #333 !important;
  color: white !important;
}
.tag-selector .multiselect__single,
.tag-selector .multiselect__input {
  background: transparent !important;
  color: white !important;
}
</style>
