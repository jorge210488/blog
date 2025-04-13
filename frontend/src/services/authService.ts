import api from "./api";

interface RegisterPayload {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  role: string;
  img_url?: string | null;
}

interface RegisterResponse {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  role: string;
  img_url: string | null;
  created_at: string;
  updated_at: string;
  credential: {
    id: string;
    auth_provider: string;
    is_verified: boolean;
  };
}

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

export const register = async ({
  first_name,
  last_name,
  email,
  password,
  role,
  img_url = null,
}: RegisterPayload): Promise<RegisterResponse> => {
  try {
    const response = await api.post<RegisterResponse>("/api/accounts/users/", {
      first_name,
      last_name,
      email,
      role,
      img_url,
      credential: {
        auth_provider: "email",
        password, // 👈 El password debe ir anidado
      },
    });

    return response.data;
  } catch (error: any) {
    console.error(
      "Error completo en register:",
      error.response?.data || error.message
    );
    throw new Error(
      "Error al registrar: " +
        JSON.stringify(error.response?.data || error.message)
    );
  }
};
