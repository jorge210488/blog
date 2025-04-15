import api from "./api";
import { useUserStore } from "../store/userStore";

const getAuthHeaders = () => {
  const userStore = useUserStore();
  const token = userStore.token;
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export interface Like {
  id: string;
  post: string;
  user: string;
  created_at: string;
}

// ✅ Obtener todos los likes (por el usuario autenticado)
export const getLikes = async (): Promise<Like[]> => {
  try {
    const response = await api.get<Like[]>("/api/interactions/likes/", {
      headers: getAuthHeaders(),
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching likes:", error);
    return [];
  }
};

export const likePost = async (postId: string): Promise<Like | null> => {
  try {
    const response = await api.post<Like>(
      "/api/interactions/likes/",
      { post: postId },
      { headers: getAuthHeaders() }
    );
    return response.data;
  } catch (error) {
    console.error(`Error liking post ${postId}:`, error);
    return null;
  }
};

export const unlikePost = async (likeId: string): Promise<boolean> => {
  try {
    await api.delete(`/api/interactions/likes/${likeId}/`, {
      headers: getAuthHeaders(),
    });
    return true;
  } catch (error) {
    console.error(`Error unliking like ${likeId}:`, error);
    return false;
  }
};

export const getLikesByPost = async (postId: string): Promise<Like[]> => {
  try {
    const response = await api.get<Like[]>(
      `/api/interactions/likes/by-post/${postId}/`,
      {
        headers: getAuthHeaders(),
      }
    );
    return response.data;
  } catch (error) {
    console.error(`Error fetching likes for post ${postId}:`, error);
    return [];
  }
};
