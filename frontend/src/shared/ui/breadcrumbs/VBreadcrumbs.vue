<script lang="ts" setup>
interface BreadcrumbsProps {
  /**
   * Массив элементов типа { to: string; label: string; icon?: IconNames },
   * которые будут отображаться в компоненте.
   */
  items: {
    to: string;
    label: string;
    disabled?: boolean;
  }[];
}

defineProps<BreadcrumbsProps>();

const emit = defineEmits<{
  click: [to: string];
}>();

const getItemClassList = (disabled?: boolean) => {
  const baseClass = 'breadcrumbs__item';

  return {
    [baseClass]: true,
    [`${baseClass}_disabled`]: disabled,
  };
};
</script>

<template>
  <ul class="breadcrumbs">
    <li v-for="(item, index) in items" :key="index" :class="getItemClassList(item.disabled)">
      <RouterLink :to="item.to" class="breadcrumbs__link" @click="emit('click', item.to)">
        {{ item.label }}
      </RouterLink>
    </li>
  </ul>
</template>

<style lang="scss">
.breadcrumbs {
  /* Sizes */
  --breadcrumbs-row-gap: 0.5rem;
  --breadcrumbs-items-gap: #{rem(12)};

  /* Colors */
  --breadcrumbs-item-color: #{$gray-700};
  --breadcrumbs-last-item-color: #{$color-light-black};
  --breadcrumbs-item-color-hover: #{$color-light-black};

  $block: &;

  display: flex;
  flex-wrap: wrap;
  align-items: center;
  row-gap: var(--breadcrumbs-row-gap);
  font-size: rem(12);

  &__item {
    & {
      position: relative;
      display: flex;
      flex-shrink: 0;
      align-items: center;
      margin-right: var(--breadcrumbs-items-gap);
      color: var(--breadcrumbs-item-color);
      transition: color $default-transition;
      white-space: nowrap;
    }

    &_disabled {
      pointer-events: none;
    }

    &:not(&_disabled) {
      @include media-hover-device-self {
        color: var(--breadcrumbs-item-color-hover);
      }
    }

    &:after {
      content: '/';
      position: absolute;
      top: 50%;
      right: calc(var(--breadcrumbs-items-gap) / -2);
      display: block;
      color: var(--breadcrumbs-item-color);
      transform: translateX(50%) translateY(-50%);
    }

    &:last-child {
      flex-shrink: initial;
      margin-right: 0;
      color: var(--breadcrumbs-last-item-color);

      &:after {
        display: none;
      }
    }
  }
}
</style>
