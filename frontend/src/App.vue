<script setup lang="ts">
import Navbar from '@/components/Navbar.vue';
import { RouterView } from 'vue-router';
console.log("This is a test.")
</script>

<template>
  <h1>This is a test</h1>
  <Navbar />
  <RouterView />
</template>