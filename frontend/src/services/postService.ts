import api from "./api";

interface Post {
  id: string;
  title: string;
  slug: string;
  content: string;
  created_at: string;
  updated_at: string;
  category: { id: string; name: string; slug: string };
  resources: Array<{ id: string; title: string; file: string }>;
}

// ✅ Obtener todos los posts (opcionalmente con filtros)
export const getPosts = async (filters?: {
  search?: string;
  category?: string;
}) => {
  try {
    const params: Record<string, string> = {};
    if (filters?.search) params["search"] = filters.search;
    if (filters?.category) params["category__slug"] = filters.category; // ✅ Filtra por slug

    const response = await api.get<Post[]>("/api/posts/", { params });
    return response.data;
  } catch (error) {
    console.error("Error fetching posts:", error);
    return [];
  }
};

// ✅ Obtener un post por su ID o slug
export const getPostById = async (id: string) => {
  try {
    const response = await api.get<Post>(`/api/posts/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching post ${id}:`, error);
    return null;
  }
};

// ✅ Obtener posts por categoría usando `slug`
export const getPostsByCategory = async (categorySlug: string) => {
  try {
    const response = await api.get<Post[]>("/api/posts/", {
      params: { category__slug: categorySlug },
    });
    return response.data;
  } catch (error) {
    console.error(`Error fetching posts for category ${categorySlug}:`, error);
    return [];
  }
};

// ✅ Crear un nuevo post
export const createPost = async (postData: FormData) => {
  try {
    const response = await api.post<Post>("/api/posts/", postData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error creating post:", error);
    return null;
  }
};

// ✅ Actualizar un post
export const updatePost = async (id: string, postData: Partial<Post>) => {
  try {
    const response = await api.put<Post>(`/api/posts/${id}/`, postData);
    return response.data;
  } catch (error) {
    console.error(`Error updating post ${id}:`, error);
    return null;
  }
};

// ✅ Eliminar un post
export const deletePost = async (id: string) => {
  try {
    await api.delete(`/api/posts/${id}/`);
    return true;
  } catch (error) {
    console.error(`Error deleting post ${id}:`, error);
    return false;
  }
};
