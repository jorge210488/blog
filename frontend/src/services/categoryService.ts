import api from "./api";

interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string;
  post_count: number; // ✅ Incluir el conteo de posts
}

interface Post {
  id: string;
  title: string;
  slug: string;
  content: string;
  created_at: string;
  updated_at: string;
}

// ✅ Obtener todas las categorías con el número de posts
export const getCategories = async () => {
  try {
    const response = await api.get<Category[]>("/api/posts/categories");
    return response.data;
  } catch (error) {
    console.error("Error fetching categories:", error);
    return [];
  }
};

// ✅ Obtener una categoría por ID
export const getCategoryById = async (id: string) => {
  try {
    const response = await api.get<Category>(`/api/posts/categories/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching category ${id}:`, error);
    return null;
  }
};

// ✅ Obtener los posts de una categoría específica usando el `slug`
export const getPostsByCategory = async (slug: string) => {
  try {
    const response = await api.get<Post[]>("/api/posts/", {
      params: { category__slug: slug }, // 🔥 Filtrar por slug
    });
    return response.data;
  } catch (error) {
    console.error(`Error fetching posts for category ${slug}:`, error);
    return [];
  }
};

// ✅ Crear una categoría
export const createCategory = async (categoryData: Partial<Category>) => {
  try {
    const response = await api.post<Category>(
      "/api/posts/categories/",
      categoryData
    );
    return response.data;
  } catch (error) {
    console.error("Error creating category:", error);
    return null;
  }
};

// ✅ Actualizar una categoría
export const updateCategory = async (
  id: string,
  categoryData: Partial<Category>
) => {
  try {
    const response = await api.put<Category>(
      `/api/posts/categories/${id}/`,
      categoryData
    );
    return response.data;
  } catch (error) {
    console.error(`Error updating category ${id}:`, error);
    return null;
  }
};

// ✅ Eliminar una categoría
export const deleteCategory = async (id: string) => {
  try {
    await api.delete(`/api/posts/categories/${id}/`);
    return true;
  } catch (error) {
    console.error(`Error deleting category ${id}:`, error);
    return false;
  }
};
