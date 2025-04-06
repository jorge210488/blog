import api from "./api";
import { useUserStore } from "../store/userStore";

export interface Resource {
  id: string;
  title: string;
  description?: string;
  file: string;
  tool?: string;
  user_id: string; // 👈 nuevo campo del dueño del recurso
  created_at?: string;
  updated_at?: string;
}

export interface ResourceFilters {
  search?: string;
  tool?: string;
  sortBy?: "updated_at" | "-updated_at"; // Ensure allowed values
}

export const getResources = async (filters?: ResourceFilters) => {
  try {
    // Build query params only with defined values
    const params: Record<string, string> = {};
    if (filters?.search) params["search"] = filters.search;
    if (filters?.tool) params["tool"] = filters.tool;
    if (filters?.sortBy) params["ordering"] = filters.sortBy;

    const response = await api.get<Resource[]>("/api/resources/", { params });
    return response.data;
  } catch (error) {
    console.error("Error fetching resources:", error);
    return [];
  }
};

export const getUserResources = async () => {
  try {
    const userStore = useUserStore(); // ✅ Get token from store

    if (!userStore.token) {
      console.error("User is not authenticated.");
      return [];
    }

    const response = await api.get<Resource[]>("/api/resources/user/", {
      headers: {
        Authorization: `Bearer ${userStore.token}`, // ✅ Add token for authentication
      },
    });

    // ✅ Asegurar que description nunca sea undefined
    return response.data.map((resource) => ({
      ...resource,
      description: resource.description ?? "", // 🔥 Asigna "" si es undefined
    }));
  } catch (error) {
    console.error("Error fetching user resources:", error);
    return [];
  }
};

export const getResourceById = async (id: string) => {
  try {
    const response = await api.get<Resource>(`/api/resources/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching resource ${id}:`, error);
    return null;
  }
};

export const createResource = async (resourceData: FormData) => {
  try {
    const userStore = useUserStore(); // ✅ Get token from store
    const response = await api.post<Resource>("/api/resources/", resourceData, {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Bearer ${userStore.token}`, // ✅ Add token
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error creating resource:", error);
    return null;
  }
};

export const updateResource = async (
  id: string,
  resourceData: Partial<Resource>
) => {
  try {
    const userStore = useUserStore(); // ✅ Get token from store
    const response = await api.put<Resource>(
      `/api/resources/${id}/`,
      resourceData,
      {
        headers: {
          Authorization: `Bearer ${userStore.token}`, // ✅ Add token
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error(`Error updating resource ${id}:`, error);
    return null;
  }
};

export const deleteResource = async (id: string) => {
  try {
    const userStore = useUserStore(); // ✅ Get token from store
    await api.delete(`/api/resources/${id}/`, {
      headers: {
        Authorization: `Bearer ${userStore.token}`, // ✅ Add token
      },
    });
    return true;
  } catch (error) {
    console.error(`Error deleting resource ${id}:`, error);
    return false;
  }
};

export const downloadResourceFile = async (id: string) => {
  try {
    const userStore = useUserStore();

    if (!userStore.token) {
      console.error("User is not authenticated.");
      return;
    }

    const response = await api.get(`/api/resources/${id}/download/`, {
      responseType: "blob", // 👈 para descargar archivos
      headers: {
        Authorization: `Bearer ${userStore.token}`,
      },
    });

    // 🔽 Descargar el archivo automáticamente en el navegador
    const blob = new Blob([response.data], { type: "application/json" });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `resource_${id}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Error downloading resource file:", error);
  }
};
