import api from "./api";
import { useUserStore } from "../store/userStore";

export interface User {
  id: string;
  first_name?: string;
  last_name?: string;
  email?: string;
  role?: string;
  img_url?: string | null;
  password?: string;
}

// ✅ Función para obtener los headers con el token
const getAuthHeaders = () => {
  const userStore = useUserStore();
  return {
    headers: {
      Authorization: `Bearer ${userStore.token}`,
    },
  };
};

export const getAllUsers = async (): Promise<User[]> => {
  try {
    const response = await api.get<User[]>(
      "/api/accounts/users/",
      getAuthHeaders()
    );
    return response.data;
  } catch (error: any) {
    console.error(
      "Error fetching users:",
      error.response?.data || error.message
    );
    throw new Error(error.response?.data?.message || "Failed to fetch users");
  }
};

export const getUserById = async (id: string): Promise<User> => {
  try {
    const response = await api.get<User>(
      `/api/accounts/users/${id}/`,
      getAuthHeaders()
    );
    return response.data;
  } catch (error: any) {
    console.error(
      "Error fetching user:",
      error.response?.data || error.message
    );
    throw new Error(error.response?.data?.message || "Failed to fetch user");
  }
};

export const updateUser = async (
  id: string,
  userData: Partial<User>
): Promise<User> => {
  try {
    // ✅ Filtramos los valores `undefined` antes de enviar a la API
    const filteredUserData = Object.fromEntries(
      Object.entries(userData).filter(([_, value]) => value !== undefined)
    );

    const response = await api.patch<User>(
      `/api/accounts/users/${id}/`,
      filteredUserData,
      getAuthHeaders()
    );
    return response.data;
  } catch (error: any) {
    console.error(
      "Error updating user:",
      error.response?.data || error.message
    );
    throw new Error(error.response?.data?.message || "Failed to update user");
  }
};

export const deleteUser = async (id: string): Promise<void> => {
  try {
    await api.delete(`/api/accounts/users/${id}/`, getAuthHeaders());
  } catch (error: any) {
    console.error(
      "Error deleting user:",
      error.response?.data || error.message
    );
    throw new Error(error.response?.data?.message || "Failed to delete user");
  }
};

export const uploadUserAvatar = async (
  userId: string,
  avatarFile: File
): Promise<string> => {
  try {
    const formData = new FormData();
    formData.append("avatar", avatarFile); // 👈 clave correcta para el endpoint

    const userStore = useUserStore();
    const response = await api.post<{ img_url: string }>(
      `/api/accounts/users/${userId}/upload-avatar/`,
      formData,
      {
        headers: {
          Authorization: `Bearer ${userStore.token}`,
          "Content-Type": "multipart/form-data", // 👈 necesario para subir archivos
        },
      }
    );

    return response.data.img_url; // ✅ Devolvemos la URL que vino del backend
  } catch (error: any) {
    console.error(
      "Error uploading avatar:",
      error.response?.data || error.message
    );
    throw new Error(error.response?.data?.message || "Failed to upload avatar");
  }
};
