// src/services/googleAuthService.ts
import api from "./api";

interface GoogleLoginResponse {
  access: string;
  refresh: string;
  user: {
    first_name: string;
    last_name: string;
    img_url?: string | null;
  };
}

export const loginWithGoogle = async (
  token: string
): Promise<GoogleLoginResponse> => {
  try {
    const response = await api.post("/api/accounts/auth/google/", {
      token,
    });
    return response.data;
  } catch (error) {
    console.error("Google login failed:", error);
    throw error;
  }
};
