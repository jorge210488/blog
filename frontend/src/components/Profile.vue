<script setup lang="ts">
import { ref, computed } from "vue";
import { useUserStore } from "../store/userStore";
import { updateUser } from "../services/userService";
import { uploadUserAvatar } from "../services/userService";

interface UserProfile {
  email: string;
  first_name: string;
  last_name: string;
  password?: string;
  confirmPassword?: string;
}

const emit = defineEmits(["close"]);
const userStore = useUserStore();

// Obtener los datos del usuario desde el store
const profile = ref({
  email: userStore.user?.email || "",
  firstName: userStore.user?.first_name || "",
  lastName: userStore.user?.last_name || "",
  password: "********",
  confirmPassword: "********",
});

const profilePicture = computed(
  () => userStore.user?.img_url || "/profile3.avif"
);

// ✅ Verifica si el usuario ingresó una nueva contraseña
const isNewPassword = computed(() => profile.value.password !== "********");

// ✅ Validación para habilitar el botón de actualización
const isPasswordValid = computed(() => {
  return (
    (!isNewPassword.value ||
      profile.value.password === profile.value.confirmPassword) &&
    profile.value.password.trim() !== ""
  );
});

// ✅ Verifica si las contraseñas no coinciden (para mostrar error)
const showPasswordError = computed(() => {
  return (
    isNewPassword.value &&
    profile.value.confirmPassword !== "********" &&
    profile.value.password !== profile.value.confirmPassword
  );
});

// ✅ Función para actualizar el perfil
const updateProfile = async () => {
  if (!isPasswordValid.value) return;

  try {
    const currentUser = userStore.user!;
    const updatedFields: Partial<UserProfile> = {};

    if (
      profile.value.firstName &&
      profile.value.firstName !== currentUser.first_name
    ) {
      updatedFields.first_name = profile.value.firstName;
    }
    if (
      profile.value.lastName &&
      profile.value.lastName !== currentUser.last_name
    ) {
      updatedFields.last_name = profile.value.lastName;
    }
    if (isNewPassword.value && profile.value.password.trim()) {
      updatedFields.password = profile.value.password;
    }

    if (Object.keys(updatedFields).length === 0) {
      console.log("No hay cambios en el perfil.");
      return;
    }

    const updatedUser = await updateUser(currentUser.id, updatedFields);

    userStore.setUser(
      userStore.token!,
      updatedUser.first_name ?? currentUser.first_name,
      updatedUser.last_name ?? currentUser.last_name,
      currentUser.img_url ?? null
    );

    console.log("Profile updated successfully:", updatedUser);
    emit("close");
  } catch (error) {
    console.error("Error updating profile:", error);
  }
};

// ✅ Limpiar campos de contraseña al hacer clic
const clearPassword = (field: "password" | "confirmPassword") => {
  if (profile.value[field] === "********") profile.value[field] = "";
};

// Placeholder para la lógica de actualización de la imagen
const updateProfilePicture = async () => {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = "image/*";

  input.onchange = async (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (!target.files || target.files.length === 0) return;

    const file = target.files[0];
    const user = userStore.user;
    if (!user) return;

    try {
      const imgUrl = await uploadUserAvatar(user.id, file);

      // ✅ Update store with new avatar
      userStore.setUser(
        userStore.token!,
        user.first_name,
        user.last_name,
        imgUrl
      );

      alert("Profile picture uploaded successfully.");
    } catch (error) {
      console.error("Error uploading avatar:", error);
      alert("Failed to upload profile picture. Please try again.");
    }
  };

  input.click(); // 👈 Trigger file input
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
      <h2 class="text-xl font-semibold text-center mb-4">Profile</h2>

      <div class="flex items-center space-x-4 mb-6">
        <div class="relative">
          <img
            :src="profilePicture"
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
            @focus="clearPassword('password')"
            :class="{ 'border-red-500': showPasswordError }"
            class="w-full px-3 py-2 bg-gray-800 rounded-lg text-white outline-none focus:ring-2 focus:ring-blue-500 border"
          />
        </div>

        <div>
          <label class="block text-sm text-gray-400">Confirm Password</label>
          <input
            type="password"
            v-model="profile.confirmPassword"
            @focus="clearPassword('confirmPassword')"
            :class="{ 'border-red-500': showPasswordError }"
            class="w-full px-3 py-2 bg-gray-800 rounded-lg text-white outline-none focus:ring-2 focus:ring-blue-500 border"
          />
          <!-- Mensaje de error si las contraseñas no coinciden -->
          <p v-if="showPasswordError" class="text-red-500 text-sm mt-1">
            Passwords must match.
          </p>
        </div>

        <div class="flex justify-between mt-4">
          <button
            @click="updateProfile"
            :disabled="!isPasswordValid"
            class="px-4 py-2 bg-blue-500 text-white rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed hover:bg-blue-600"
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
