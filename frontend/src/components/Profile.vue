<script setup lang="ts">
import { ref } from "vue";

const emit = defineEmits(["close"]);

const profile = ref({
  email: "jorgemartinez@example.com",
  firstName: "",
  lastName: "",
  password: "",
  confirmPassword: "",
});

const updateProfile = () => {
  console.log("Profile updated", profile.value);
};

const closeModal = () => {
  emit("close");
};

// Placeholder for the image update logic
const updateProfilePicture = () => {
  console.log("Profile picture update triggered");
};
</script>

<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50"
    @click.self="closeModal"
  >
    <div class="bg-gray-900 text-white p-6 rounded-2xl shadow-lg w-[500px]">
      <h2 class="text-xl font-semibold text-center mb-4">Profile</h2>

      <div class="flex items-center space-x-4 mb-6">
        <div class="relative">
          <img
            src="/profile.jpg"
            alt="Profile"
            class="w-24 h-24 rounded-full border-2 border-gray-400 cursor-pointer transition-transform transform hover:scale-150"
            @click="updateProfilePicture"
          />
        </div>
        <div>
          <p class="text-sm text-gray-400">Email</p>
          <p class="font-semibold">{{ profile.email }}</p>
        </div>
      </div>

      <div class="space-y-4">
        <div class="flex space-x-4">
          <div class="w-1/2">
            <label class="block text-sm text-gray-400">First Name</label>
            <input
              type="text"
              v-model="profile.firstName"
              class="w-full px-3 py-2 bg-gray-800 rounded-lg text-white outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div class="w-1/2">
            <label class="block text-sm text-gray-400">Last Name</label>
            <input
              type="text"
              v-model="profile.lastName"
              class="w-full px-3 py-2 bg-gray-800 rounded-lg text-white outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm text-gray-400">Password</label>
          <input
            type="password"
            v-model="profile.password"
            class="w-full px-3 py-2 bg-gray-800 rounded-lg text-white outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block text-sm text-gray-400">Confirm Password</label>
          <input
            type="password"
            v-model="profile.confirmPassword"
            class="w-full px-3 py-2 bg-gray-800 rounded-lg text-white outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div class="flex justify-between mt-4">
          <button
            @click="updateProfile"
            class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
          >
            Update
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
