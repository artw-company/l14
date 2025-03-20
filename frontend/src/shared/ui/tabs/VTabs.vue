<script setup lang="ts" generic="Value extends string | number">
interface Props {
  list: {
    label: string;
    value: Value;
  }[];
}

withDefaults(defineProps<Props>(), {});

const modelValue = defineModel<Value>();
</script>

<template>
  <ul class="tabs">
    <li
      class="tabs__item"
      :class="{ tabs__item_active: modelValue === item.value }"
      v-for="item in list"
      :key="item.value"
    >
      {{ item.label }}
    </li>
  </ul>
</template>

<style lang="scss" scoped>
.tabs {
  overflow: auto;
  display: flex;
  align-items: center;
  flex-wrap: nowrap;

  &__item {
    padding: rem(8) rem(16);
    border-bottom: rem(2) solid $gray-300;
    font-size: rem(15);
    white-space: nowrap;
    color: $color-light-black;
    transition: border-color $default-transition;
    cursor: pointer;
    user-select: none;

    &:hover {
      border-color: $gray-600;
    }

    &_active {
      font-weight: 600;
      border-color: $color-light-black;
      pointer-events: none;
    }
  }
}
</style>
