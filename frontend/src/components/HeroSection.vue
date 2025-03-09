<script setup lang="ts">
import { ref } from "vue";

// Función para formatear la fecha actual
const formatDate = (date: Date) => {
  const meses = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
  ];
  const day = date.getDate();
  const month = meses[date.getMonth()];
  const year = date.getFullYear();
  return `${month} ${day}, ${year}`;
};

// Se obtiene la fecha actual formateada
const currentDate = ref(formatDate(new Date()));
</script>

<template>
  <section class="relative w-full h-[70vh] sm:h-[90vh] overflow-hidden">
    <!-- Video de fondo -->
    <video class="w-full h-full object-cover" autoplay muted loop playsinline>
      <source src="/IA.mp4" type="video/mp4" />
      Tu navegador no soporta la reproducción de videos.
    </video>

    <!-- Capa de superposición -->
    <div
      class="absolute inset-0 bg-black bg-opacity-40 flex flex-col justify-center items-center text-white text-center"
    >
      <h1 class="text-xl sm:text-5xl font-bold sm:pt-0 pt-10 sm:px-4 sm:py-2">
        SOBRE LA INTELIGENCIA ARTIFICIAL
      </h1>
      <h2 class="text-2xl sm:text-3xl font-bold px-4 py-2 mt-2">IA AGENTS</h2>
      <span class="text-lg italic bg-pink-300 px-4 py-1 rounded-lg mt-4">
        {{ currentDate }}
      </span>
    </div>

    <!-- Degradado mejorado para fusión más suave -->
    <div
      class="absolute bottom-0 w-full h-96 bg-gradient-to-b from-transparent via-[#0b1622] to-[#0b1622] opacity-90 mix-blend-overlay blur-md"
    ></div>
  </section>
</template>
