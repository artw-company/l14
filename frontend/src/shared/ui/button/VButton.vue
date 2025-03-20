<script setup lang="ts">
import { computed } from 'vue';

import { VIconBase } from '../icon-base';
import { VSpinner } from '../spinner';

import type { ButtonProps } from './types';

const props = withDefaults(defineProps<ButtonProps>(), {
  size: 'md',
  theme: 'primary',
  icon: null,
  disabled: false,
  loading: false,
  active: false,
});

const slot = defineSlots();

const classList = computed(() => {
  const baseClass = 'button';

  return {
    [baseClass]: true,
    [`${baseClass}_size_${props.size}`]: props.size,
    [`${baseClass}_theme_${props.theme}`]: props.theme,
    [`${baseClass}_disabled`]: props.disabled,
    [`${baseClass}_loading`]: props.loading,
    [`${baseClass}_active`]: props.active,
    [`${baseClass}_only-icon`]: props.icon && !slot.default,
  };
});
</script>

<template>
  <button :class="classList" :disabled="disabled">
    <span class="button__wrapper">
      <span class="button__inner">
        <span v-if="slot.default" class="button__text">
          <slot></slot>
        </span>

        <VIconBase v-if="icon" :key="icon" class="button__icon" :name="icon" />
      </span>

      <Transition name="fade">
        <VSpinner v-if="loading" class="button__spinner" />
      </Transition>
    </span>
  </button>
</template>

<style lang="scss">
.button {
  /* General */
  --button-display: inline-flex;
  --button-align-items: center;
  --button-justify-content: center;
  --button-disabled-opacity: 0.3;

  /* Sizes */
  --button-padding-x: 14px;
  --button-padding-y: 12px;
  --button-height: auto;
  --button-border-radius: 8px;
  --button-border-width: 1px;
  --button-icon-gap: 8px;
  --button-icon-size: 24px;
  --button-spinner-size: 24px;
  --button-font-size: 16px;

  /* Colors */
  --button-color: #000;
  --button-bg-color: #fff;
  --button-border-color: #000;
  --button-hover-color: #000;
  --button-hover-bg-color: #ddd;
  --button-hover-border-color: #aaa;
  --button-active-color: #000;
  --button-active-bg-color: #ddd;
  --button-active-border-color: #aaa;
  --button-disabled-color: #000;
  --button-disabled-bg-color: #fff;
  --button-disabled-border-color: #000;

  $block: &;

  display: var(--button-display);
  overflow: hidden;
  height: var(--button-height);
  box-sizing: border-box;
  align-items: var(--button-align-items);
  justify-content: var(--button-justify-content);
  padding: var(--button-padding-y) var(--button-padding-x);
  border: var(--button-border-width) solid var(--button-border-color);
  border-radius: var(--button-border-radius);
  background-color: var(--button-bg-color);
  font-size: var(--button-font-size);
  color: var(--button-color);
  transition: $default-transition;
  transition-property: background-color, border-color, color, opacity;
  user-select: none;

  @include media-hover-device-self {
    border-color: var(--button-hover-border-color);
    background-color: var(--button-hover-bg-color);
    color: var(--button-hover-color);
  }

  &_size {
    &_sm {
      --button-padding-x: #{rem(5)};
      --button-padding-y: #{rem(5)};
      --button-height: #{rem(24)};
      --button-border-radius: 50%;
      --button-border-width: 0;
      --button-icon-gap: #{rem(8)};
      --button-icon-size: #{rem(14)};
      --button-spinner-size: #{rem(14)};
      --button-font-size: #{rem(13)};
    }

    &_md {
      --button-padding-x: #{rem(20)};
      --button-padding-y: #{rem(10)};
      --button-height: #{rem(36)};
      --button-border-radius: #{rem(20)};
      --button-border-width: 0;
      --button-icon-gap: #{rem(10)};
      --button-icon-size: #{rem(16)};
      --button-spinner-size: #{rem(16)};
      --button-font-size: #{rem(13)};
    }
  }

  &_theme {
    &_primary {
      --button-color: #{$color-white};
      --button-bg-color: #{$color-primary};
      --button-border-color: transparent;
      --button-hover-color: #{$color-white};
      --button-hover-bg-color: #{$color-dark-primary};
      --button-hover-border-color: transparent;
      --button-active-color: #{$color-white};
      --button-active-bg-color: #{$color-dark-primary};
      --button-active-border-color: transparent;
      --button-disabled-color: #{$color-white};
      --button-disabled-bg-color: #{$color-primary};
      --button-disabled-border-color: transparent;
      --button-disabled-opacity: 0.3;
    }

    &_secondary,
    &_secondary-black {
      --button-color: #{$color-primary};
      --button-bg-color: #{$color-white};
      --button-border-color: transparent;
      --button-hover-color: #{$color-white};
      --button-hover-bg-color: #{$color-primary};
      --button-hover-border-color: transparent;
      --button-active-color: #{$color-white};
      --button-active-bg-color: #{$color-primary};
      --button-active-border-color: transparent;
      --button-disabled-color: #{$color-primary};
      --button-disabled-bg-color: #{$color-white};
      --button-disabled-border-color: transparent;
      --button-disabled-opacity: 0.3;
    }

    &_secondary-black {
      --button-color: #{$color-light-black};
    }
  }

  &:active,
  &_active {
    border-color: var(--button-active-border-color);
    background-color: var(--button-active-bg-color);
    color: var(--button-active-color);
  }

  &:visited {
    color: var(--button-color);
  }

  /* Mods */
  &:disabled,
  &_disabled {
    border-color: var(--button-disabled-border-color);
    background-color: var(--button-disabled-bg-color);
    color: var(--button-disabled-color);
    opacity: var(--button-disabled-opacity);
    pointer-events: none;
  }

  &_loading {
    pointer-events: none;

    #{$block}__inner {
      opacity: 0;
    }
  }

  &_only-icon {
    padding: 0;
    aspect-ratio: 1 / 1;

    &:deep(.icon) {
      flex-shrink: 0;
    }

    #{$block}__inner & {
      gap: 0;
    }
  }

  /* Elements */
  &__wrapper {
    position: relative;
    display: flex;
  }

  &__inner {
    display: flex;
    width: 100%;
    align-items: center;
    justify-content: center;
    gap: var(--button-icon-gap);
    transition: opacity $default-transition;
  }

  &__text {
    display: flex;
    align-items: center;
  }

  &__icon {
    width: var(--button-icon-size);
    height: var(--button-icon-size);
  }

  &__spinner {
    position: absolute;
    top: 50%;
    left: 50%;
    width: var(--button-spinner-size);
    height: var(--button-spinner-size);
    color: inherit;
    transform: translate(-50%, -50%);
  }
}
</style>
