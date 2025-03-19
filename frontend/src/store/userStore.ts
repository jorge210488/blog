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
    showLoginModal: false, // ✅ Controla la apertura del modal de login
  }),

  getters: {
    isAuthenticated: (state) => !!state.token, // ✅ Simplifica la verificación de autenticación
  },

  actions: {
    // ✅ Método para establecer el usuario cuando inicia sesión
    setUser(
      token: string,
      first_name: string,
      last_name: string,
      img_url: string | null
    ) {
      this.token = token;
      localStorage.setItem("access_token", token);

      // Decodificar el token para obtener `id`, `email` y `role`
      const decoded = jwtDecode<TokenPayload>(token);

      this.user = {
        id: decoded.user_id,
        email: decoded.email,
        role: decoded.role,
        first_name,
        last_name,
        img_url: img_url || null,
      };

      this.showLoginModal = false; // Cerrar modal si estaba abierto
    },

    // ✅ Método para cerrar sesión
    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    },

    // ✅ Método para abrir el modal cuando se intente acceder a una página protegida
    requireLogin() {
      this.showLoginModal = true;
    },
  },

  persist: true, // ✅ Mantiene la sesión después de recargar la página
});
