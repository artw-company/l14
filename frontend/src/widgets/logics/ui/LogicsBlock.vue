<script setup lang="ts">
import { ref, computed, onBeforeUnmount } from 'vue';
import type { Block } from '../types';
import { VIconBase } from '@/shared/ui/icon-base';

interface BlockOptions {
  width?: number;
  scale?: number;
  titleHeight?: number;
  center?: {
    x: number;
    y: number;
  };
}

interface Props extends Block {
  selected: boolean;
  options: BlockOptions;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  (e: 'select'): void;
  (e: 'linkingBreakOrigin', index: number): void;
  (e: 'linkingStart', index: number): void;
  (e: 'linkingStop'): void;
  (e: 'linkingBreak'): void;
}>();

const x = defineModel<number>('x', { required: true });
const y = defineModel<number>('y', { required: true });

const mouseX = ref(0);
const mouseY = ref(0);

const lastMouseX = ref(0);
const lastMouseY = ref(0);

const dragging = ref(false);
const hasDragged = ref(false);

const handleMove = (e: MouseEvent) => {
  mouseX.value = e.pageX || e.clientX + document.documentElement.scrollLeft;
  mouseY.value = e.pageY || e.clientY + document.documentElement.scrollTop;

  if (dragging.value) {
    const diffX = mouseX.value - lastMouseX.value;
    const diffY = mouseY.value - lastMouseY.value;

    lastMouseX.value = mouseX.value;
    lastMouseY.value = mouseY.value;

    moveWithDiff(diffX, diffY);
    hasDragged.value = true;
  }
};

const handleDown = (e: MouseEvent) => {
  mouseX.value = e.pageX || e.clientX + document.documentElement.scrollLeft;
  mouseY.value = e.pageY || e.clientY + document.documentElement.scrollTop;

  lastMouseX.value = mouseX.value;
  lastMouseY.value = mouseY.value;

  dragging.value = true;
  emit('select');

  document.documentElement.addEventListener('mousemove', handleMove, true);
  document.documentElement.addEventListener('mouseup', handleUp, true);
};

const handleUp = () => {
  if (dragging.value) {
    dragging.value = false;

    if (hasDragged.value) {
      hasDragged.value = false;
    }
  }

  document.documentElement.removeEventListener('mousemove', handleMove, true);
  document.documentElement.removeEventListener('mouseup', handleUp, true);
};

const slotMouseDown = (index: number) => {
  emit('linkingBreakOrigin', index);
  emit('linkingStart', index);
};

const slotMouseUp = () => {
  emit('linkingStop');
};

const slotBreak = () => {
  emit('linkingBreak');
};

const moveWithDiff = (diffX: number, diffY: number) => {
  const sc = props.options.scale ?? 1;
  x.value = x.value + diffX / sc;
  y.value = y.value + diffY / sc;
};

const blockStyle = computed(() => {
  const sc = props.options.scale ?? 1;
  const center = props.options.center || { x: 0, y: 0 };

  return {
    top: center.y + y.value * sc + 'px',
    left: center.x + x.value * sc + 'px',
    width: (props.options.width ?? 200) + 'px',
    transform: `scale(${sc})`,
  };
});

const titleHeight = computed(() =>
  props.options.titleHeight ? `${props.options.titleHeight}px` : 'auto',
);

onBeforeUnmount(() => {
  document.documentElement.removeEventListener('mousemove', handleMove, true);
  document.documentElement.removeEventListener('mouseup', handleUp, true);
});
</script>

<template>
  <div
    class="logics-block"
    :class="{ 'logics-block_selected': selected }"
    :style="blockStyle"
    @mousedown.prevent="handleDown"
  >
    <header class="logics-block__header">
      <span class="logics-block__header-text">
        {{ title }}
      </span>
    </header>

    <div class="logics-block__wrapper">
      <div class="logics-block__input">
        <div
          class="logics-block__circle"
          :class="{ 'logics-block__circle_active': inputs?.[0]?.active }"
          @mousedown.stop.prevent="slotBreak"
          @mouseup.stop.prevent="slotMouseUp"
        ></div>
      </div>

      <div class="logics-block__outputs">
        <div class="logics-block__output" v-for="(slot, index) in outputs" :key="index">
          {{ slot.label }}

          <div
            class="logics-block__circle logics-block__circle_output"
            :class="{
              'logics-block__circle_active': slot.active,
              'logics-block__circle_checkbox': type === 'checkbox',
            }"
            @mousedown.stop.prevent="slotMouseDown(index)"
          >
            <VIconBase
              v-if="type === 'checkbox'"
              class="logics-block__circle-check"
              size="custom"
              name="check"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
$blockBorder: 1px;

$slotPaddingInner: 2px 0;
$slotHeight: 16px;

$inputCircleSize: 12px;
$outputCircleSize: 8px;

$circleNewColor: $color-dark-primary;
$circleRemoveColor: #ffa09b;
$circleConnectedColor: $color-primary;

.logics-block {
  $block: &;

  position: absolute;
  background: $gray-200;
  z-index: 1;
  opacity: 0.95;
  cursor: move;
  border: $blockBorder solid transparent;
  border-radius: 8px;
  transform-origin: top left;

  &_selected {
    border-color: $color-primary;
    z-index: 2;
  }

  &__header {
    display: flex;
    align-items: center;
    background: $color-primary;
    padding: 16px 16px 13px;
    height: v-bind(titleHeight);
    border-radius: 8px 8px 0 0;
    font-size: 12px;
    color: #fff;

    &-text {
      @include text-clamp(2);
    }
  }

  &__wrapper {
    position: relative;
    display: flex;
    padding: 12px 8px 16px 16px;
  }

  &__outputs {
    padding: $slotPaddingInner;
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 10px;
  }

  &__input {
    position: absolute;
    top: 24px;
    left: 0;
    transform: translateX(-50%);
  }

  &__outputs {
    flex: 1;
  }

  &__circle {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
    width: $inputCircleSize;
    height: $inputCircleSize;
    border: 1px solid $color-primary;
    border-radius: 100%;
    background-color: $color-white;
    cursor: crosshair;
    transition: $default-transition;
    transition-property: background-color, border-color;

    &_output {
      width: $outputCircleSize;
      height: $outputCircleSize;
    }

    &_active {
      background: $circleConnectedColor;
      border-color: $color-white;
    }

    &_checkbox {
      border-radius: 20%;
    }

    &_checkbox {
      &#{$block}__circle_active {
        background-color: $circleConnectedColor;
        border-color: $circleConnectedColor;
      }
    }

    &-check {
      fill: $color-white;
      width: $outputCircleSize * 0.6;
      height: $outputCircleSize * 0.6;
    }
  }

  &__output {
    overflow: hidden;
    display: flex;
    justify-content: space-between;
    align-items: center;

    #{$block}__circle {
      @include increase-click-area(5);

      &:hover {
        background-color: $circleNewColor;
      }

      &_active {
        &:hover {
          background-color: rgba($circleConnectedColor, 0.4);
        }
      }
    }
  }
}
</style>
