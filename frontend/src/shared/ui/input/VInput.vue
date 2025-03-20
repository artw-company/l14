<script setup lang="ts">
import { computed, ref, useAttrs } from 'vue';

import { VIconBase } from '../icon-base';

import type { InputIconItem, InputProps } from './types';

// Attrs
defineOptions({
  inheritAttrs: false,
});

const props = withDefaults(defineProps<InputProps>(), {
  placeholder: '',
  disabled: false,
  readonly: false,
  type: 'text',
  mask: '',
  prependIcon: undefined,
  appendIcon: undefined,
});

// Events
const emit = defineEmits<{
  'update:modelValue': [value: string];
  blur: [];
  focus: [];
  prependIconClick: [];
  appendIconClick: [];
}>();

const slots = defineSlots();

const modelValue = defineModel<string>({ required: true });
const inputRef = ref<HTMLInputElement | null>(null);

const { class: classes, ...attrs } = useAttrs();

const isTouched = ref(false);
const isFocused = ref(false);

const classList = computed(() => {
  const baseClass = 'input';

  return {
    [baseClass]: true,
    [`${baseClass}_focused`]: isFocused.value,
    [`${baseClass}_disabled`]: props.disabled,
    [`${baseClass}_prependIcon`]: isPrependIcon.value,
    [`${baseClass}_appendIcon`]: isAppendIcon.value,
  };
});

const onFocus = () => {
  isFocused.value = true;
  emit('focus');
};

const onBlur = () => {
  isFocused.value = false;

  if (!isTouched.value) {
    isTouched.value = true;
  }

  emit('blur');
};

/**
 * Управление иконками
 */
const isPrependIcon = computed(() => Boolean(slots['prepend-icon'] || props.prependIcon));
const isAppendIcon = computed(() => Boolean(slots['append-icon'] || props.appendIcon));

const getIconClasses = (icon: InputIconItem) => {
  const baseClass = 'input__icon-item';

  const additionalClasses = {
    [`${baseClass}_type_button`]: icon.clickable,
  };

  return [baseClass, additionalClasses];
};

/**
 * Обработчики событий
 */
const onInput = (event: InputEvent | Event) => {
  const target = event.target as HTMLInputElement;
  const val = target.value;

  emit('update:modelValue', val);
};

const onClickIconBox = () => {
  if (inputRef.value) {
    inputRef.value.focus();
  }
};

const onIconClick = (type: 'append' | 'prepend' | 'label') => {
  switch (type) {
    case 'append':
      emit('appendIconClick');
      break;
    case 'prepend':
      emit('prependIconClick');
      break;
  }
};

const onEnter = () => {
  if (inputRef.value) {
    inputRef.value.blur();
  }
};
</script>

<template>
  <div :class="[classList, classes]">
    <div class="input__inner">
      <slot name="prepend">
        <div
          v-if="isPrependIcon"
          class="input__icon-box input__icon-box_disabled input__icon-box_type_prepend"
        >
          <slot name="prepend-icon">
            <VIconBase
              v-if="prependIcon"
              :class="getIconClasses(prependIcon)"
              :name="prependIcon.name"
              @click="onIconClick('prepend')"
            />
          </slot>
        </div>
      </slot>

      <input
        :id="name"
        ref="inputRef"
        class="input__native"
        :name="name"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :readonly="readonly"
        v-bind="attrs"
        @input="onInput"
        @focus="onFocus"
        @blur="onBlur"
        @keydown.enter="onEnter"
      />

      <slot name="append">
        <div
          v-if="isAppendIcon"
          class="input__icon-box input__icon-box_type_append"
          @click="onClickIconBox"
        >
          <slot name="append-icon">
            <VIconBase
              v-if="appendIcon"
              :class="getIconClasses(appendIcon)"
              :name="appendIcon.name"
              @click="onIconClick('append')"
            />
          </slot>
        </div>
      </slot>
    </div>
  </div>
</template>

<style lang="scss">
.input {
  /* Indents */
  --input-inner-padding-x: #{rem(14)};
  --input-inner-padding-y: #{rem(11)};
  --input-border-radius: #{rem(30)};
  --input-border-width: #{rem(1)};
  --input-icon-size: #{rem(16)};
  --input-icon-gap: #{rem(10)};
  --input-font-size: #{rem(13)};

  /* Colors */
  --input-text-color: #{$gray-900};
  --input-border-color: #{$gray-200};
  --input-background-color: #{$gray-200};
  --input-placeholder-color: #{$gray-700};

  /* Hover */
  --input-text-color-hover: #{$gray-900};
  --input-border-color-hover: #{$gray-700};
  --input-background-color-hover: #{$gray-200};

  /* Focus */
  --input-text-color-focus: #{$gray-900};
  --input-border-color-focus: #{$gray-900};
  --input-background-color-focus: #{$gray-200};

  $block: &;
  $icon-padding: calc(
    var(--input-inner-padding-x, 0) + var(--input-icon-size, 0) + var(--input-icon-gap, 0)
  );

  color: var(--input-text-color);
  text-align: left;

  // Mods
  @include media-hover-device-self {
    color: var(--input-text-color-hover);

    #{$block}__inner {
      border-color: var(--input-border-color-hover);
    }

    #{$block}__inner {
      background-color: var(--input-background-color-hover);
    }
  }

  &_focused {
    color: var(--input-text-color-focus);

    #{$block}__inner {
      border-color: var(--input-border-color-focus);
    }

    #{$block}__inner {
      background-color: var(--input-background-color-focus);
    }
  }

  &_disabled {
    pointer-events: none;
    user-select: none;

    #{$block}__inner {
      opacity: 0.5;
    }

    #{$block}__icon-item {
      pointer-events: none;
    }
  }

  // Elements
  &__inner {
    position: relative;
    overflow: hidden;
    width: 100%;
    border: var(--input-border-width) solid var(--input-border-color);
    border-radius: var(--input-border-radius);
    font-size: var(--input-font-size);
    transition: $default-transition;
    transition-property: border-color, color;
  }

  &__native {
    &::placeholder {
      color: var(--input-placeholder-color);
    }

    & {
      width: 100%;
      padding: var(--input-inner-padding-y) var(--input-inner-padding-x);
      background-color: var(--input-background-color);
      color: inherit;
      transition: color $default-transition;

      #{$block}_prependIcon & {
        padding-left: $icon-padding;
      }

      #{$block}_appendIcon & {
        padding-right: $icon-padding;
      }
    }
  }

  &__label-icon {
    width: var(--input-label-icon-size);
    height: var(--input-label-icon-size);
    margin-left: auto;
    cursor: pointer;
    transition: opacity $default-transition;

    @include media-hover-device-self {
      opacity: 0.6;
    }
  }

  &__icon {
    &-box {
      position: absolute;
      top: 50%;
      display: flex;
      cursor: text;
      gap: var(--input-icon-gap);
      transform: translateY(-50%);

      &_type {
        &_prepend {
          left: var(--input-inner-padding-x);
        }

        &_append {
          right: var(--input-inner-padding-x);
        }
      }
    }

    &-item {
      width: var(--input-icon-size);
      height: var(--input-icon-size);
      pointer-events: none;

      &_type {
        &_button {
          cursor: pointer;
          pointer-events: auto;
          transition: opacity $default-transition;

          @include media-hover-device-self {
            opacity: 0.6;
          }
        }
      }
    }
  }
}
</style>
