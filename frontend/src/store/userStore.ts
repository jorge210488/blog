import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
  state: () => ({
    user: null as { name: string } | null,
  }),
  actions: {
    setUser(user: { name: string }) {
      this.user = user;
    },
  },
});
