import { defineStore } from "pinia";
import { jwtDecode } from "jwt-decode";

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  img_url?: string | null;
}

interface TokenPayload {
  user_id: string;
  email: string;
  role: string;
  exp: number;
}

export const useUserStore = defineStore("user", {
  state: () => ({
    user: null as User | null,
    token: localStorage.getItem("access_token") || null,
  }),
  actions: {
    setUser(
      token: string,
      first_name: string,
      last_name: string,
      img_url: string | null
    ) {
      this.token = token;
      localStorage.setItem("access_token", token);

      // Desencriptar el token para obtener `id`, `email` y `role`
      const decoded = jwtDecode<TokenPayload>(token);

      this.user = {
        id: decoded.user_id,
        email: decoded.email,
        role: decoded.role,
        first_name,
        last_name,
        img_url: img_url || null,
      };
    },
    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    },
  },
  persist: true,
});
