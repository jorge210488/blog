<template>
  <button :class="`btn ${typeClass}`" :disabled="disabled">
    <slot></slot>
  </button>
</template>

<script lang="ts">
export default {
  props: {
    type: {
      type: String,
      default: "primary",
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    typeClass(): string {
      return this.type === "primary" ? "btn-primary" : "btn-secondary";
    },
  },
};
</script>

<style scoped>
.btn {
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
}
.btn-primary {
  background-color: #007bff;
  color: white;
}
.btn-secondary {
  background-color: #6c757d;
  color: white;
}
</style>
