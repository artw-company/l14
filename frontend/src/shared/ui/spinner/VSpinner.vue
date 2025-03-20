<script setup lang="ts">
import { computed } from 'vue';
import { VIconBase } from '../icon-base';

export interface SpinnerProps {
  iconName?: string;
}

withDefaults(defineProps<SpinnerProps>(), {
  iconName: 'spinner',
});

const classes = computed(() => ['ui-spinner']);
</script>

<template>
  <span :class="classes">
    <VIconBase class="spinner__icon" :name="iconName" />
  </span>
</template>

<style lang="scss" scoped>
.spinner {
  --spinner-size: 24px;

  display: inline-block;
  width: var(--spinner-size);
  height: var(--spinner-size);

  &__icon {
    display: block;
    width: 100%;
    height: 100%;
    animation: rotate360 1s linear infinite;
  }

  @keyframes rotate360 {
    0% {
      transform: rotate(0);
    }

    100% {
      transform: rotate(360deg);
    }
  }
}
</style>
