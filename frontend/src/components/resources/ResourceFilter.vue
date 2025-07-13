<script setup lang="ts">
import { ref, defineEmits, watch } from "vue";
import ResourceUploadModal from "./ResourceUploadModal.vue";

const search = ref("");
const selectedTool = ref("");
const sortBy = ref<"-updated_at" | "updated_at">("-updated_at");
const resourceScope = ref<"all" | "mine">("all");
const showUploadModal = ref(false);

const emit = defineEmits(["filter"]);

const applyFilters = () => {
  emit("filter", {
    search: search.value || undefined,
    tool: selectedTool.value || undefined,
    sortBy: sortBy.value,
    owner: resourceScope.value === "mine" ? "me" : undefined,
  });
};

const openModal = () => {
  document.body.style.overflow = "hidden";
  showUploadModal.value = true;
};

const closeModal = () => {
  document.body.style.overflow = "";
  showUploadModal.value = false;
};

watch(showUploadModal, (value) => {
  if (!value) document.body.style.overflow = "";
});
</script>

<template>
  <!-- ✅ VERSIÓN DESKTOP -->
  <div
    class="hidden md:flex bg-black/40 backdrop-blur-xl border border-white/30 p-4 rounded-lg shadow-lg flex-col sm:flex-row sm:items-center gap-4 mx-auto md:w-3/4"
  >
    <input
      v-model="search"
      @input="applyFilters"
      type="text"
      placeholder="🔎 Search Resource..."
      class="w-full p-3 rounded-md bg-transparent border border-white/40 text-white placeholder-gray-400 focus:outline-none focus:border-blue-400"
    />

    <div class="flex flex-col sm:flex-row gap-4 w-full">
      <select
        v-model="selectedTool"
        @change="applyFilters"
        class="custom-select w-full sm:w-auto"
      >
        <option value="">All Tools</option>
        <option value="AgentHub">AgentHub</option>
        <option value="AgentOps">AgentOps</option>
        <option value="AutoGPT">AutoGPT</option>
        <option value="Custom">Custom</option>
        <option value="Dialogflow">Dialogflow</option>
        <option value="Flowise">Flowise</option>
        <option value="Go High Level">Go High Level</option>
        <option value="LangChain">LangChain</option>
        <option value="Make">Make</option>
        <option value="n8n">n8n</option>
        <option value="Other">Other</option>
        <option value="Pipedream">Pipedream</option>
        <option value="Relevance AI">Relevance AI</option>
        <option value="Retell AI">Retell AI</option>
        <option value="Stack AI">Stack AI</option>
        <option value="TaskMagic">TaskMagic</option>
        <option value="Tiledesk">Tiledesk</option>
        <option value="Voiceflow">Voiceflow</option>
        <option value="Wit.ai">Wit.ai</option>
        <option value="Zapier">Zapier</option>
      </select>

      <select
        v-model="sortBy"
        @change="applyFilters"
        class="custom-select w-full sm:w-auto"
      >
        <option :value="'-updated_at'">Newest</option>
        <option :value="'updated_at'">Oldest</option>
      </select>

      <select
        v-model="resourceScope"
        @change="applyFilters"
        class="custom-select w-full sm:w-auto"
      >
        <option value="all">All Resources</option>
        <option value="mine">My Resources</option>
      </select>

      <button
        @click="openModal"
        class="custom-select bg-blue-500 text-white hover:bg-blue-600 transition w-full sm:w-auto"
      >
        + Add Resource
      </button>
    </div>
  </div>

  <!-- ✅ VERSIÓN MOBILE -->
  <div class="block md:hidden space-y-4 mt-4">
    <input
      v-model="search"
      @input="applyFilters"
      type="text"
      placeholder="🔎 Search Resource..."
      class="w-full p-3 rounded-md bg-transparent border border-white/40 text-white placeholder-gray-400 focus:outline-none focus:border-blue-400"
    />

    <div class="flex gap-4">
      <select
        v-model="selectedTool"
        @change="applyFilters"
        class="custom-select w-1/2"
      >
        <option value="">All Tools</option>
        <option value="Relevance AI">Relevance AI</option>
        <option value="Make">Make</option>
        <option value="n8n">n8n</option>
        <option value="Other">Other</option>
      </select>

      <select
        v-model="sortBy"
        @change="applyFilters"
        class="custom-select w-1/2"
      >
        <option :value="'-updated_at'">Newest</option>
        <option :value="'updated_at'">Oldest</option>
      </select>
    </div>

    <div class="flex gap-4">
      <select
        v-model="resourceScope"
        @change="applyFilters"
        class="custom-select w-1/2"
      >
        <option value="all">All Resources</option>
        <option value="mine">My Resources</option>
      </select>

      <button
        @click="openModal"
        class="custom-select bg-blue-500 text-white hover:bg-blue-600 transition w-1/2"
      >
        + Add
      </button>
    </div>
  </div>

  <!-- Modal bloqueando fondo -->
  <Teleport to="body">
    <div
      v-if="showUploadModal"
      class="fixed inset-0 z-[9999] bg-black/90 backdrop-blur-sm flex items-center justify-center"
      @click.self="closeModal"
    >
      <div class="z-[10000] w-full max-w-xl">
        <ResourceUploadModal @close="closeModal" />
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.custom-select {
  background-color: transparent !important;
  border: 1px solid rgba(255, 255, 255, 0.4);
  color: white;
  padding: 12px;
  border-radius: 6px;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  cursor: pointer;
  min-width: 150px;
}

.custom-select option {
  background-color: black !important;
  color: white !important;
}

.custom-select:focus {
  border-color: #4299e1;
  outline: none;
}
</style>
