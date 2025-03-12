import api from "./api";

interface LoginResponse {
  refresh: string;
  access: string;
  user: {
    id: string;
    email: string;
    first_name: string;
    last_name: string;
    role: string;
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
    return response.data;
  } catch (error: any) {
    console.error(
      "Login error:",
      error.response?.data?.message || error.message
    );
    throw new Error(error.response?.data?.message || "Login failed");
  }
};
