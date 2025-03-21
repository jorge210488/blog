import api from "./api";

// ✅ Obtener todas las etiquetas (tags)
export const getTags = async () => {
  try {
    const response = await api.get("/api/tags/");
    return response.data;
  } catch (error) {
    console.error("Error fetching tags:", error);
    return [];
  }
};
