<script setup lang="ts">
import { TheSidebar } from '@/widgets/sidebar';
import { TheHeader } from '@/widgets/header';
</script>

<template>
  <div class="default-layout">
    <TheSidebar class="default-layout__sidebar" />

    <div class="default-layout__wrapper">
      <TheHeader />

      <main class="default-layout__main">
        <slot></slot>
      </main>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.default-layout {
  display: flex;
  width: 100%;
  height: 100vh;

  &__sidebar {
    flex-shrink: 0;
  }

  &__wrapper {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
  }

  &__main {
    overflow: auto;
    flex: 1;
  }
}
</style>
