import { defineStore } from "pinia";

export const useMainStore = defineStore("main", {
  state: () => ({
    user: null as string | null,
  }),
  actions: {
    setUser(user: string) {
      this.user = user;
    },
  },
});
