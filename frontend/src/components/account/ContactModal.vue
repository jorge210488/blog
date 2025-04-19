<script setup lang="ts">
import { ref, computed } from "vue";
import { useUserStore } from "../../store/userStore";
import { sendContactMessage } from "../../services/contactService";

const emit = defineEmits(["close"]);
const userStore = useUserStore();

const user = userStore.user!;

const subject = ref("");
const message = ref("");
const altEmail = ref("");
const phone = ref("");
const isLoading = ref(false);

const profilePicture = computed(() => user.img_url || "/profile3.avif");
const email = computed(() => user.email || "");

const isValid = computed(() => subject.value.trim() && message.value.trim());

const handleSubmit = async () => {
  if (!isValid.value) return;

  isLoading.value = true;
  try {
    await sendContactMessage({
      subject: subject.value,
      message: message.value,
      alt_email: altEmail.value || undefined,
      phone: phone.value || undefined,
    });

    alert("Message sent successfully.");
    emit("close");
  } catch (err) {
    console.error(err);
    alert("Failed to send message. Try again.");
  } finally {
    isLoading.value = false;
  }
};

const closeModal = () => {
  emit("close");
};
</script>

<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50"
    @click.self="closeModal"
  >
    <div class="bg-gray-900 text-white p-6 rounded-2xl shadow-lg w-[500px]">
      <h2 class="text-xl font-semibold text-center mb-4">Contact</h2>

      <!-- Imagen y email -->
      <div class="flex items-center space-x-4 mb-6">
        <img
          :src="profilePicture"
          alt="Profile"
          class="w-24 h-24 rounded-full border-2 border-gray-400 object-cover"
        />
        <div>
          <p class="text-sm text-gray-400">Email</p>
          <p class="font-semibold break-all">{{ email }}</p>
        </div>
      </div>

      <!-- Formulario -->
      <div class="space-y-4">
        <div>
          <label class="block text-sm text-gray-400">Subject</label>
          <input
            v-model="subject"
            type="text"
            class="w-full px-3 py-2 bg-gray-800 rounded-lg text-white outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block text-sm text-gray-400">Message</label>
          <textarea
            v-model="message"
            rows="4"
            class="w-full px-3 py-2 bg-gray-800 rounded-lg text-white outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          ></textarea>
        </div>

        <div class="flex space-x-4">
          <div class="w-1/2">
            <label class="block text-sm text-gray-400"
              >Alternative Email (optional)</label
            >
            <input
              v-model="altEmail"
              type="email"
              class="w-full px-3 py-2 bg-gray-800 rounded-lg text-white outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div class="w-1/2">
            <label class="block text-sm text-gray-400"
              >Phone Number (optional)</label
            >
            <input
              v-model="phone"
              type="tel"
              class="w-full px-3 py-2 bg-gray-800 rounded-lg text-white outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <div class="flex justify-between mt-4">
          <button
            @click="handleSubmit"
            :disabled="!isValid || isLoading"
            class="px-4 py-2 bg-blue-500 text-white rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed hover:bg-blue-600"
          >
            Send
          </button>
          <button
            @click="closeModal"
            class="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
