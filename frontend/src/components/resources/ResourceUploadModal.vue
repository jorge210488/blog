<script setup lang="ts">
import { ref } from "vue";
import { useToast } from "vue-toastification";
import { createResource } from "../../services/resourceService"; // ✅ Import the service

const toast = useToast();
const emit = defineEmits(["close", "upload"]);

const jsonFile = ref<File | null>(null);
const title = ref<string>("");
const description = ref<string>("");
const tool = ref<string>("Relevance AI");

// Tool options
const toolOptions = [
  "Relevance AI",
  "Retell AI",
  "Make",
  "n8n",
  "Flowise",
  "LangChain",
  "Voiceflow",
  "Dialogflow",
  "Wit.ai",
  "AgentOps",
  "AutoGPT",
  "Custom",
  "Other",
];

// ✅ Handle selected JSON file
const handleFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (!input.files || input.files.length === 0) return;

  const file = input.files[0];
  if (!file.name.endsWith(".json")) {
    toast.error("Only JSON files are allowed. ❌");
    return;
  }

  jsonFile.value = file; // Only one JSON file is allowed
};

// ✅ Upload resource to the backend using the service
const uploadResource = async () => {
  if (!jsonFile.value) {
    toast.error("You must select a JSON file. ❌");
    return;
  }
  if (!title.value.trim()) {
    toast.error("Title is required. ❌");
    return;
  }
  if (!description.value.trim()) {
    toast.error("Description is required. ❌");
    return;
  }
  if (!tool.value.trim()) {
    toast.error("You must select a tool. ❌");
    return;
  }

  try {
    // ✅ Create FormData
    const formData = new FormData();
    formData.append("title", title.value);
    formData.append("description", description.value);
    formData.append("tool", tool.value);
    formData.append("file", jsonFile.value);

    // ✅ Call the createResource service
    const uploadedResource = await createResource(formData);

    if (!uploadedResource) {
      throw new Error("Resource upload failed.");
    }

    // ✅ Emit only the resource ID to `postForm`
    emit("upload", {
      id: uploadedResource.id,
      title: title.value,
      description: description.value,
      tool: tool.value,
    });

    toast.success("Resource uploaded successfully! ✅");

    // ✅ Clear form for further uploads
    jsonFile.value = null;
    title.value = "";
    description.value = "";
    tool.value = "Relevance AI";

    // ✅ Close the modal after upload
    emit("close");
  } catch (error) {
    toast.error("Error uploading resource. ❌");
  }
};
</script>

<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
  >
    <div class="bg-gray-900 p-6 rounded-lg shadow-lg w-96">
      <h2 class="text-white text-xl mb-4">Upload JSON Resource</h2>

      <!-- Title -->
      <div class="mb-4">
        <label class="text-white">Title:</label>
        <input
          type="text"
          v-model="title"
          class="w-full text-black p-2 rounded"
          placeholder="Enter a title"
        />
      </div>

      <!-- Description -->
      <div class="mb-4">
        <label class="text-white">Description:</label>
        <textarea
          v-model="description"
          class="w-full text-black p-2 rounded"
          placeholder="Enter a description"
        ></textarea>
      </div>

      <!-- Select Tool -->
      <div class="mb-4">
        <label class="text-white">Tool:</label>
        <select v-model="tool" class="w-full text-black p-2 rounded">
          <option v-for="option in toolOptions" :key="option" :value="option">
            {{ option }}
          </option>
        </select>
      </div>

      <!-- Upload JSON -->
      <div class="mb-4">
        <label class="text-white">JSON File:</label>
        <input
          type="file"
          accept=".json"
          @change="handleFileChange"
          class="w-full text-white"
        />
      </div>

      <!-- Buttons -->
      <div class="flex justify-between mt-4">
        <button
          @click="uploadResource"
          class="bg-green-500 text-white px-4 py-2 rounded"
        >
          Upload
        </button>
        <button
          @click="$emit('close')"
          class="bg-red-500 text-white px-4 py-2 rounded"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>
