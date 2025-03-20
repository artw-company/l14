<script setup lang="ts">
import { VInput } from '@/shared/ui/input';
import { ref } from 'vue';
import { VIconBase } from '@/shared/ui/icon-base';

const search = ref('');
</script>

<template>
  <header class="header">
    <VInput
      class="header__input"
      name="search"
      v-model="search"
      :prepend-icon="{ name: 'search' }"
      placeholder="Искать пользователя, опрос"
    />

    <div class="header__profile">
      <RouterLink class="header__profile-icon default-link" to="/">
        <VIconBase name="bell" size="lg" />
      </RouterLink>

      <RouterLink class="header__user default-link" to="/">
        <img class="header__user-avatar" src="/images/avatar.png" alt="Аватар пользователя" />
        <div class="header__user-info">
          <span class="header__user-name">Молодова В. И.</span>
          <span class="header__user-post">Администратор</span>
        </div>
      </RouterLink>
    </div>
  </header>
</template>

<style lang="scss" scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: $header-h;
  padding: rem(16) rem(20) rem(16) rem(40);

  &__input {
    width: rem(438);
  }

  &__profile {
    display: flex;
    align-items: center;
    gap: rem(24);

    &-icon {
      position: relative;
      display: block;
      color: $gray-400;

      &:after {
        content: '';
        position: absolute;
        top: rem(2);
        right: rem(3);
        width: rem(5);
        height: rem(5);
        border-radius: 50%;
        background-color: $color-primary;
      }
    }
  }

  &__user {
    display: flex;
    align-items: center;
    gap: rem(10);

    &-avatar {
      overflow: hidden;
      width: rem(36);
      height: rem(36);
      border-radius: 50%;
    }

    &-name {
      font-size: rem(13);
      color: $color-light-black;
    }

    &-info {
      display: flex;
      flex-direction: column;
    }

    &-post {
      font-size: rem(11);
      color: $gray-400;
    }
  }
}
</style>
