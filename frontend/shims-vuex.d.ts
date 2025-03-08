// src/shims-vuex.d.ts
declare module "vuex" {
  import { Store } from "vuex";
  export * from "vuex";
  export default Store;
}
