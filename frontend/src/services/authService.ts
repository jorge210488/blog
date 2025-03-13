import api from "./api";

interface LoginResponse {
  refresh: string;
  access: string;
  user: {
    first_name: string;
    last_name: string;
    img_url: string;
  };
}

export const login = async (
  email: string,
  password: string
): Promise<LoginResponse> => {
  try {
    const response = await api.post<LoginResponse>("/api/accounts/login/", {
      email,
      password,
    });

    console.log("Respuesta completa del backend:", response.data);
    if (!response.data || !response.data.access || !response.data.user) {
      throw new Error(
        "Error: La respuesta de la API no contiene los datos esperados."
      );
    }

    return response.data;
  } catch (error: any) {
    console.error("Error en login:", error.response?.data || error.message);
    throw new Error(error.response?.data?.message || "Login failed");
  }
};
