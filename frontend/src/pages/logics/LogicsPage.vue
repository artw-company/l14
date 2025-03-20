<script setup lang="ts">
import { onBeforeMount, ref, shallowRef } from 'vue';
import { type Question, SurveyClient } from '@/entities/Survey';
import { VBreadcrumbs } from '@/shared/ui/breadcrumbs';
import { VButton } from '@/shared/ui/button';
import { VTabs } from '@/shared/ui/tabs';
import { LogicsBlocksContainer, useSceneData } from '@/widgets/logics';
import { VSpinner } from '@/shared/ui/spinner';

// Id опроса, константой, так как реализована только одна демо-страница логики опросов
const SURVEY_ID = 1;

const surveyName = ref('');
const questions = shallowRef<Question[]>([]);
const isLoading = ref(false);
const isInit = ref(false);

const { blocks, links, exportOriginData } = useSceneData(questions);

const breadcrumbs = [
  { label: 'Главная', to: '/' },
  { label: 'Создать опрос', to: '/' },
];

const activeTab = ref('logic');
const tabs = [
  { label: 'Вопросы', value: 'questions' },
  { label: 'Параметры', value: 'parameters' },
  { label: 'Логика', value: 'logic' },
  { label: 'Условия', value: 'conditions' },
  { label: 'Респонденты', value: 'respondents' },
];

const onSave = async () => {
  try {
    isLoading.value = true;
    const questions = exportOriginData();

    await SurveyClient.put(SURVEY_ID, {
      id: SURVEY_ID,
      name: surveyName.value,
      questions,
    });
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};

const fetchData = async () => {
  try {
    isLoading.value = true;
    const { data } = await SurveyClient.get(SURVEY_ID);
    questions.value = data.questions;
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};

onBeforeMount(async () => {
  await fetchData();
  isInit.value = true;
});
</script>

<template>
  <div class="survey-page">
    <div class="survey-page__header">
      <h1 class="survey-page__title">Создание опроса</h1>
      <VBreadcrumbs :items="breadcrumbs" />
    </div>

    <div class="survey-page__controls">
      <VTabs v-model="activeTab" :list="tabs" />

      <div class="survey-page__buttons">
        <VButton theme="secondary" :loading="isLoading" @click="onSave"> Сохранить </VButton>
        <VButton icon="arrow-tail-right" :loading="isLoading" @click="onSave"> Отправить </VButton>
        <VButton theme="secondary-black" icon="dots-vertical" />
      </div>
    </div>

    <Transition name="fade" mode="out-in">
      <LogicsBlocksContainer
        v-if="isInit"
        class="survey-page__container"
        v-model:blocks="blocks"
        v-model:links="links"
      />
      <div v-else class="survey-page__container survey-page__container_empty">
        <VSpinner class="survey-page__spinner" />
      </div>
    </Transition>
  </div>
</template>

<style lang="scss" scoped>
.survey-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: rem(25) rem(20) rem(10) rem(40);
  background-color: $gray-200;

  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  &__title {
    font-size: rem(24);
    font-weight: 600;
  }

  &__controls {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: rem(10) 0 rem(16);
  }

  &__buttons {
    display: flex;
    align-items: center;
    gap: rem(16);
  }

  &__container {
    width: 100%;
    height: 100%;
    background-color: $color-white;
    box-shadow: 0 rem(10) rem(20) rgba(18, 38, 63, 0.0313726);
    border-radius: rem(10);

    &_empty {
      position: relative;
    }
  }

  &__spinner {
    position: absolute;
    top: 50%;
    left: 50%;
    width: rem(64);
    height: rem(64);
    color: $gray-900;
    transform: translate(-50%, -50%);
  }
}
</style>
