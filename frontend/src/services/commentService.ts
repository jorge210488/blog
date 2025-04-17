import api from "./api";
import { useUserStore } from "../store/userStore";

// Interface matching your Comment model
export interface Comment {
  id: string;
  post: string; // post ID
  user: string; // user ID or email, depending on backend
  content: string;
  parent_comment?: string | null; // optional parent
  created_at: string;
  updated_at: string;
  replies?: Comment[]; // only on GET
}

// Auth headers
const getAuthHeaders = () => {
  const userStore = useUserStore();
  const token = userStore.token;
  return token ? { Authorization: `Bearer ${token}` } : {};
};

// 🔹 Get all comments for a post (including 1 level of replies)
export const getCommentsByPost = async (postId: string): Promise<Comment[]> => {
  try {
    const response = await api.get<Comment[]>(
      `/api/interactions/comments/by-post/${postId}/`,
      { headers: getAuthHeaders() }
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching comments:", error);
    return [];
  }
};

// 🔹 Create a new comment (optional parent)
export const createComment = async (commentData: {
  post: string;
  content: string;
  parent_comment?: string;
}): Promise<Comment | null> => {
  try {
    const response = await api.post<Comment>(
      "/api/interactions/comments/",
      commentData,
      {
        headers: getAuthHeaders(),
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error creating comment:", error);
    return null;
  }
};

// 🔹 Update a comment (only content)
export const updateComment = async (
  commentId: string,
  content: string
): Promise<Comment | null> => {
  try {
    const response = await api.put<Comment>(
      `/api/interactions/comments/${commentId}/`,
      { content },
      { headers: getAuthHeaders() }
    );
    return response.data;
  } catch (error) {
    console.error(`Error updating comment ${commentId}:`, error);
    return null;
  }
};

// 🔹 Delete a comment
export const deleteComment = async (commentId: string): Promise<boolean> => {
  try {
    await api.delete(`/api/interactions/comments/${commentId}/`, {
      headers: getAuthHeaders(),
    });
    return true;
  } catch (error) {
    console.error(`Error deleting comment ${commentId}:`, error);
    return false;
  }
};
