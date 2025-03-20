<script setup lang="ts">
// Пока нет логики или пропсов
import { ref } from 'vue';
import { VIconBase } from '@/shared/ui/icon-base';
import { VButton } from '@/shared/ui/button';

const menuItems = [
  { name: 'Дашборд', icon: 'dashboard', link: '/' },
  { name: 'Опросы', icon: 'reports', link: '/', active: true },
  { name: 'Пользователи', icon: 'staff', link: '/' },
];

const additionalMenuItems = [
  { name: 'Настройки', icon: 'settings', link: '/' },
  { name: 'Мгновенная поддержка', icon: 'headphone-sound', link: '/' },
];

const footerItem = { name: 'Выйти', icon: 'logout' };

const isCompact = ref(false);
</script>

<template>
  <aside class="sidebar" :class="{ sidebar_compact: isCompact }">
    <header class="sidebar__header">
      <RouterLink to="/" class="sidebar__logo-wrapper default-link">
        <Transition name="fade" mode="out-in">
          <img
            v-if="!isCompact"
            key="full"
            class="sidebar__logo"
            src="/images/logo.svg"
            alt="Логотип"
          />

          <img
            v-else
            key="compact"
            class="sidebar__logo sidebar__logo_compact"
            src="/images/logo-short.svg"
            alt="Логотип"
          />
        </Transition>
      </RouterLink>

      <VButton
        class="sidebar__button"
        :class="{ sidebar__button_compact: isCompact }"
        icon="arrow-left"
        size="sm"
        @click="isCompact = !isCompact"
      />
    </header>

    <div class="sidebar__wrapper">
      <h2 class="sidebar__title">Меню</h2>

      <nav class="sidebar__nav">
        <ul class="sidebar__nav-list">
          <li class="sidebar__nav-item" v-for="(item, index) in menuItems" :key="index">
            <RouterLink
              :to="item.link"
              class="sidebar__nav-item-inner"
              :class="{ 'sidebar__nav-item-inner_active': item.active }"
            >
              <VIconBase class="sidebar__nav-icon" :name="item.icon" />

              <Transition name="fade">
                <span v-show="!isCompact" class="sidebar__nav-text">{{ item.name }}</span>
              </Transition>
            </RouterLink>
          </li>
        </ul>

        <ul class="sidebar__nav-list sidebar__nav-list_additional">
          <li class="sidebar__nav-item" v-for="(item, index) in additionalMenuItems" :key="index">
            <RouterLink :to="item.link" class="sidebar__nav-item-inner">
              <VIconBase class="sidebar__nav-icon" :name="item.icon" />

              <Transition name="fade">
                <span v-show="!isCompact" class="sidebar__nav-text">{{ item.name }}</span>
              </Transition>
            </RouterLink>
          </li>
        </ul>
      </nav>

      <footer class="sidebar__footer">
        <div class="sidebar__nav-item">
          <div class="sidebar__nav-item-inner">
            <VIconBase class="sidebar__nav-icon" :name="footerItem.icon" />
            <Transition name="fade">
              <span v-show="!isCompact" class="sidebar__nav-text">{{ footerItem.name }}</span>
            </Transition>
          </div>
        </div>

        <p class="sidebar__copyright">2025 Логотип. Все права защищены</p>
      </footer>
    </div>
  </aside>
</template>

<style scoped lang="scss">
.sidebar {
  $block: &;

  display: flex;
  flex-direction: column;
  width: rem(252);
  height: 100%;
  background: $color-dark-primary;
  transition: width $default-transition;

  &_compact {
    width: rem(60);

    #{$block}__button {
      transform: translateX(50%) rotate(180deg);
    }

    #{$block}__title {
      height: rem(0);
    }

    #{$block}__nav-text {
      visibility: hidden;
      opacity: 0;
    }

    #{$block}__nav-item-inner {
      gap: 0;
    }

    #{$block}__copyright {
      height: 0;
    }
  }

  &__header {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    height: $header-h;
  }

  &__button {
    --button-border-width: #{rem(1.5)};
    --button-border-color: #{$color-white};
    --button-hover-border-color: #{$color-white};
    --button-active-border-color: #{$color-white};

    position: absolute;
    right: 0;
    box-sizing: content-box;
    transform: translateX(50%);
    transition: all $default-transition;
  }

  &__logo {
    width: rem(159);
    transition: all $default-transition;

    &_compact {
      width: rem(20);
    }
  }

  &__wrapper {
    overflow: hidden;
    display: flex;
    flex-direction: column;
    flex: 1;
    padding: rem(20);
  }

  &__title {
    overflow: hidden;
    height: rem(12);
    margin-bottom: rem(10);
    font-size: rem(11);
    font-weight: 600;
    line-height: 1.1;
    text-transform: uppercase;
    color: $gray-600;
    transition: height $default-transition;
  }

  &__card {
    background: rgba(255, 255, 255, 0.1);
  }

  &__nav {
    display: flex;
    flex-direction: column;
    flex: 1;
  }

  &__nav-list {
    display: flex;
    flex-direction: column;
    gap: rem(4);

    &_additional {
      margin-top: auto;
    }
  }

  &__nav-item-inner {
    display: flex;
    align-items: center;
    gap: rem(10);
    padding: rem(10);
    margin: 0 rem(-10);
    border-radius: rem(10);
    color: $gray-600;
    font-size: rem(13);
    transition: $default-transition;
    cursor: pointer;
    transition-property: background-color, color, gap;

    @include media-hover-device-self {
      background-color: rgba($color-white, 0.1);
      color: $color-white;
    }

    &_active {
      background-color: rgba($color-white, 0.1);
      color: $color-white;
    }
  }

  &__nav-icon {
    flex-shrink: 0;
  }

  &__nav-text {
    white-space: nowrap;
    transition: $default-transition;
    transition-property: visibility, opacity;
  }

  &__footer {
    margin-top: rem(6);
    padding-top: rem(6);
    border-top: rem(1) solid rgba($color-white, 0.3);
  }

  &__copyright {
    overflow: hidden;
    height: rem(13);
    margin-top: rem(10);
    font-size: rem(11);
    color: $gray-600;
    white-space: nowrap;
    transition: height $default-transition;
  }
}
</style>
