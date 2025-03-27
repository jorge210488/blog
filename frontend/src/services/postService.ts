import api from "./api";
import { useUserStore } from "../store/userStore"; // 🔥 Importa el store para obtener el token

// 🔥 Interfaces detalladas basadas en tu backend
interface Category {
  id: string;
  name: string;
  slug: string;
}

export interface Tag {
  id: string;
  name: string;
  slug: string;
}

interface Resource {
  id: string;
  title: string;
  file: string; // 🔥 URL del archivo en S3
}

interface Image {
  id: string;
  image_url: string; // 🔥 URL de la imagen en S3
}

export interface Post {
  id: string;
  title: string;
  slug: string;
  content: string;
  author: string;
  category: Category;
  tags: Tag[];
  images: Image[];
  resources: Resource[]; // ✅ AÑADIDO
  video_url?: string;
  views: number;
  status: "draft" | "published";
  created_at: string;
  updated_at: string;
}

// 🔥 Función para obtener los headers con autenticación
const getAuthHeaders = () => {
  const userStore = useUserStore(); // 🔥 Accede al store
  const token = userStore.token; // 🔥 Obtiene el token
  return token ? { Authorization: `Bearer ${token}` } : {};
};

// ✅ Obtener todos los posts con filtros opcionales
export const getPosts = async (filters?: {
  search?: string;
  category?: string;
}) => {
  try {
    const params: Record<string, string> = {};
    if (filters?.search) params["search"] = filters.search;
    if (filters?.category) params["category__slug"] = filters.category;

    const response = await api.get<Post[]>("/api/posts/posts/", {
      params,
      headers: getAuthHeaders(), // 🔥 Agregar autenticación
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching posts:", error);
    return [];
  }
};

// ✅ Obtener un post por su ID o slug
export const getPostById = async (id: string) => {
  try {
    const response = await api.get<Post>(`/api/posts/${id}/`, {
      headers: getAuthHeaders(), // 🔥 Agregar autenticación
    });
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
      headers: getAuthHeaders(), // 🔥 Agregar autenticación
    });
    return response.data;
  } catch (error) {
    console.error(`Error fetching posts for category ${categorySlug}:`, error);
    return [];
  }
};

// ✅ Crear un nuevo post (usa `FormData` para imágenes y archivos)
export const createPost = async (postData: FormData) => {
  try {
    // 🔥 Ver qué se está enviando exactamente
    for (let [key, value] of postData.entries()) {
      console.log(`📤 Sending: ${key} ->`, value);
    }

    const response = await api.post<Post>("/api/posts/posts/", postData, {
      headers: {
        "Content-Type": "multipart/form-data",
        ...getAuthHeaders(), // 🔥 Agregar autenticación
      },
    });

    return response.data;
  } catch (error) {
    console.error("Error creating post:", error);
    return null;
  }
};

// ✅ Actualizar un post (maneja imágenes opcionales)
export const updatePost = async (
  id: string,
  postData: Partial<Post | FormData>
) => {
  try {
    let authHeaders = getAuthHeaders(); // 🔥 Obtener headers de autenticación

    let headers: Record<string, string> = {};
    if (authHeaders.Authorization) {
      headers["Authorization"] = authHeaders.Authorization; // ✅ Solo agregar si existe
    }

    if (postData instanceof FormData) {
      headers["Content-Type"] = "multipart/form-data"; // ✅ Para archivos
    } else {
      headers["Content-Type"] = "application/json"; // ✅ Para JSON
    }

    const response = await api.put<Post>(`/api/posts/${id}/`, postData, {
      headers,
    });
    return response.data;
  } catch (error) {
    console.error(`Error updating post ${id}:`, error);
    return null;
  }
};

// ✅ Eliminar un post
export const deletePost = async (id: string) => {
  try {
    await api.delete(`/api/posts/${id}/`, {
      headers: getAuthHeaders(), // 🔥 Agregar autenticación
    });
    return true;
  } catch (error) {
    console.error(`Error deleting post ${id}:`, error);
    return false;
  }
};
