<script setup lang="ts">
import { computed, defineAsyncComponent, shallowRef, watch } from 'vue';

interface Props {
  name: string;
  size?: 'sm' | 'md' | 'lg' | 'custom';
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
});

const classList = computed(() => {
  const baseClass = 'icon';

  return {
    [baseClass]: true,
    [`${baseClass}_size_${props.size}`]: props.size,
  };
});

const icon = shallowRef();

const created = () => {
  icon.value = defineAsyncComponent({
    loader: () => import(`@/assets/icons/${props.name}.svg`),
    suspensible: false,
  });
};

try {
  created();
} catch (err) {
  console.error(err);
}

watch(
  () => props.name,
  (newValue) => {
    icon.value = defineAsyncComponent({
      loader: () => import(`@/assets/icons/${newValue}.svg`),
      suspensible: false,
    });
  },
);
</script>

<template>
  <span :class="classList">
    <component :is="icon" />
  </span>
</template>

<style lang="scss">
.icon {
  display: inline-flex;
  aspect-ratio: 1 / 1;
  color: inherit;

  &_size {
    &_sm {
      width: rem(14);
    }

    &_md {
      width: rem(20);
    }

    &_lg {
      width: rem(22);
    }
  }
}
</style>
