import api from "./api";

interface Resource {
  id: string;
  title: string;
  description?: string;
  tool: string;
  file: string;
  created_at: string;
  updated_at: string;
}

export const getResources = async (filters?: {
  search?: string;
  tool?: string;
  sortBy?: string;
}) => {
  try {
    const response = await api.get<Resource[]>("/resources/", {
      params: filters,
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching resources:", error);
    return [];
  }
};

export const getResourceById = async (id: string) => {
  try {
    const response = await api.get<Resource>(`/resources/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching resource ${id}:`, error);
    return null;
  }
};

export const createResource = async (resourceData: FormData) => {
  try {
    const response = await api.post<Resource>("/resources/", resourceData, {
      headers: {
        "Content-Type": "multipart/form-data",
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
    const response = await api.put<Resource>(`/resources/${id}/`, resourceData);
    return response.data;
  } catch (error) {
    console.error(`Error updating resource ${id}:`, error);
    return null;
  }
};

export const deleteResource = async (id: string) => {
  try {
    await api.delete(`/resources/${id}/`);
    return true;
  } catch (error) {
    console.error(`Error deleting resource ${id}:`, error);
    return false;
  }
};
