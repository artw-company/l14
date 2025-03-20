<script setup lang="ts">
/**
 * Основной контейнер для блок-схемы:
 *   - хранит и редактирует позиции/масштаб "сцены"
 *   - обрабатывает создание/разрыв связей
 *   - отслеживает состояние "выбранного" блока
 *   - организует отрисовку линий между блоками (через VueLinks)
 */

import { ref, computed, watch, onMounted, onBeforeUnmount, reactive } from 'vue';
import { debounce, getMousePosition } from '@/shared/utils';

import LogicsBlock from './LogicsBlock.vue';
import LogicsLinks from './LogicsLinks.vue';

import type { Block, Link, LineData } from '../types';

/* ===================== Пропсы и события ===================== */
const props = withDefaults(
  defineProps<{
    minScale?: number;
    maxScale?: number;
  }>(),
  {
    minScale: 0.2,
    maxScale: 5,
  },
);

const emit = defineEmits<{
  blockSelect: [payload: Block];
  blockDeselect: [payload: Block];
}>();

const blocks = defineModel<Block[]>('blocks', { required: true });
const links = defineModel<Link[]>('links', { required: true });
const container = ref({
  centerX: 0,
  centerY: 0,
  scale: 1,
});

/* ===================== Вычисляемые значения ===================== */

/** Масштаб сцены, привязанный к container.value.scale */
const scale = computed({
  get: () => container.value.scale,
  set: (val) => (container.value.scale = val),
});

/** Положение "центра" сцены, управляем через container.value.centerX/centerY */
const center = computed({
  get: () => ({
    x: container.value.centerX,
    y: container.value.centerY,
  }),
  set: (val) => {
    container.value.centerX = val.x;
    container.value.centerY = val.y;
  },
});

/** Опции, пробрасываемые дочерним VueBlock: размеры, масштаб, центр */
const optionsForChild = computed(() => {
  return {
    width: 198,
    titleHeight: 57,
    scale: scale.value,
    center: center.value,
  };
});

/** Собираем список линий (lines) на основе связей (links) и позиций блоков */
const lines = computed(() => {
  const result: LineData[] = [];

  for (const link of links.value) {
    const originBlock = blocks.value.find((b) => b.id === link.originId);
    const targetBlock = blocks.value.find((b) => b.id === link.targetId);

    if (!originBlock || !targetBlock) {
      console.error('Remove invalid link', link);
      removeLink(link.id);
      continue;
    }
    if (originBlock.id === targetBlock.id) {
      console.error('Loop detected, remove link', link);
      removeLink(link.id);
      continue;
    }

    const originPos = getConnectionPos(originBlock, link.originSlot, false);
    const targetPos = getConnectionPos(targetBlock, 0, true);

    if (!originPos || !targetPos) {
      console.error('Remove invalid link (slot not exist)', link);
      removeLink(link.id);
      continue;
    }

    result.push({
      x1: originPos.x,
      y1: originPos.y,
      x2: targetPos.x,
      y2: targetPos.y,
      style: {
        stroke: '#ADB5BD',
        strokeWidth: 2 * scale.value,
        fill: 'none',
      },
      outlineStyle: {
        stroke: '#666',
        strokeWidth: 6 * scale.value,
        strokeOpacity: 0.6,
        fill: 'none',
      },
    });
  }

  // Если есть временная линия - добавим её к списку
  if (tempLink.value) {
    result.push(tempLink.value);
  }
  return result;
});

/* ===================== DOM, реактивные переменные ===================== */

/** Ссылка на DOM-элемент контейнера, чтобы отследить клики, размеры и позицию */
const containerElement = ref<HTMLElement | null>(null);

/** Текущее положение мыши и положение мыши на предыдущем шаге */
const mousePos = reactive({ x: 0, y: 0 });
const lastMousePos = reactive({ x: 0, y: 0 });

/** Флаг для контроля перетаскивания сцены */
const dragging = ref(false);

/** Временная линия (отрисовывается во время создания новой связи) */
const tempLink = ref<LineData | null>(null);

/** Режим протягивания (создания связи), сохраняем стартовый блок и слот */
const linking = ref(false);
const linkStartData = ref<{
  block: Block;
  slotNumber: number;
} | null>(null);

/** Ссылка на "первый" блок и "выбранный" блок (опционально) */
const firstBlock = ref<Block | null>(null);
const selectedBlock = ref<Block | null>(null);

/* ===================== Методы ===================== */

/** Проверка, выбран ли блок */
const isSelectedBlock = (block: Block | null) => {
  if (!block?.id || !selectedBlock.value?.id) {
    return false;
  }
  return block.id === selectedBlock.value.id;
};

/** Выбор нового блока (сняв выбор со старого) */
const blockSelect = (block: Block) => {
  blockDeselect();
  selectedBlock.value = block;
  emit('blockSelect', block);
};

/** Снять выделение с текущего выбранного блока */
const blockDeselect = () => {
  if (selectedBlock.value) {
    emit('blockDeselect', selectedBlock.value);
  }
  selectedBlock.value = null;
};

/** Удалить связь по её ID */
const removeLink = (linkId: number | string) => {
  links.value = links.value.filter((l) => l.id !== linkId);
};

/** Обновляет флаги active у входных/выходных слотов на основании ссылок */
const prepareBlocksLinking = (blocksArr: Block[], linksArr: Link[]): Block[] => {
  // Храним активность в Set для быстрого поиска
  const activeSlots = linksArr.reduce(
    (res, link) => {
      if (link.targetId !== null) {
        res.inputs.add(link.targetId);
      }
      if (link.originId !== null && link.originSlot !== null) {
        res.outputs.add(`${link.originId}_${link.originSlot}`);
      }
      return res;
    },
    { inputs: new Set<number>(), outputs: new Set<string>() },
  );

  return blocksArr.map((block) => {
    block.inputs.forEach((inp) => {
      inp.active = activeSlots.inputs.has(inp.id);
    });
    block.outputs.forEach((out, idx) => {
      out.active = activeSlots.outputs.has(`${block.id}_${idx}`);
    });
    return block;
  });
};

/**
 * Получает координаты "слота" блока (с учётом масштаба и центра),
 * чтобы отрисовать линию с нужного места
 */
const getConnectionPos = (block: Block, slotNumber: number, isInput: boolean) => {
  if (!block || slotNumber === -1) {
    return undefined;
  }

  let x = block.x;
  let y = block.y;

  // Сдвиг на высоту заголовка
  y += optionsForChild.value.titleHeight;

  // Смещаем x вправо, если слот выходной
  if (isInput && block.inputs[slotNumber]) {
    y += 10;
    x -= 5;
  } else if (!isInput && block.outputs[slotNumber]) {
    x += optionsForChild.value.width - 9;
  } else {
    console.error('slot ' + slotNumber + ' not found, is input: ' + isInput, block);
    return undefined;
  }

  // Смещение по y, чтобы "слоты" не налезали друг на друга
  y += 12 / 2 + 12 + 3; // мелкие отступы
  y += 20 * slotNumber;

  // Учёт масштаба и центра
  x *= scale.value;
  y *= scale.value;
  x += center.value.x;
  y += center.value.y;

  return { x, y };
};

/* ===================== Обработчики событий мыши ===================== */

/**
 * handleMove:
 *   - отвечает за перетаскивание "сцены" (при зажатой ЛКМ)
 *   - обновляет позицию временной линии (tempLink), если идёт соединение
 */
const handleMove = (e: MouseEvent) => {
  if (!containerElement.value) return;
  const mouse = getMousePosition(containerElement.value, e);
  mousePos.x = mouse.x;
  mousePos.y = mouse.y;

  if (dragging.value) {
    const diffX = mousePos.x - lastMousePos.x;
    const diffY = mousePos.y - lastMousePos.y;

    lastMousePos.x = mousePos.x;
    lastMousePos.y = mousePos.y;

    container.value.centerX += diffX;
    container.value.centerY += diffY;
  }

  if (linking.value && linkStartData.value) {
    const linkStartPos = getConnectionPos(
      linkStartData.value.block,
      linkStartData.value.slotNumber,
      false,
    );
    if (linkStartPos) {
      tempLink.value = {
        x1: linkStartPos.x,
        y1: linkStartPos.y,
        x2: mousePos.x,
        y2: mousePos.y,
        style: {
          stroke: '#8f8f8f',
          strokeWidth: 4 * scale.value,
          fill: 'none',
        },
      };
    }
  }
};

/**
 * handleDown:
 *   - начинает перетаскивание сцены, если кликнули по пустому месту контейнера
 *   - снимает выделение с блока
 */
const handleDown = (e: MouseEvent) => {
  const target = e.target as HTMLElement;
  if (!containerElement.value) return;

  // Проверка: клик в свободном месте
  if (target === containerElement.value && e.buttons === 1) {
    dragging.value = true;

    const mouse = getMousePosition(containerElement.value, e);
    mousePos.x = mouse.x;
    mousePos.y = mouse.y;
    lastMousePos.x = mousePos.x;
    lastMousePos.y = mousePos.y;

    blockDeselect();
    e.preventDefault();
  }
};

/**
 * handleUp:
 *   - завершает перетаскивание сцены
 *   - сбрасывает linking, если связь не была доведена до блока
 */
const handleUp = (e: MouseEvent) => {
  const target = e.target as HTMLElement;

  if (dragging.value) {
    dragging.value = false;
  }

  // Если отпустили в контейнере и не завершили связь
  if (containerElement.value && containerElement.value.contains(target)) {
    setTimeout(() => {
      linking.value = false;
      tempLink.value = null;
      linkStartData.value = null;
    }, 0);
  }
};

/**
 * handleWheel:
 *   - масштабирование (zoom) по колёсику мыши
 *   - ограничивает масштаб props.minScale / props.maxScale
 *   - пересчитывает координаты "центра" для масштабирования относительно позиции курсора
 */
const handleWheel = (e: WheelEvent) => {
  if (!containerElement.value) return;
  const target = e.target as HTMLElement;
  if (containerElement.value.contains(target)) {
    const deltaScale = Math.pow(1.1, e.deltaY * -0.01);
    scale.value *= deltaScale;

    // Ограничения масштабирования
    if (scale.value < props.minScale) {
      scale.value = props.minScale;
      return;
    } else if (scale.value > props.maxScale) {
      scale.value = props.maxScale;
      return;
    }

    // Смещаем центр, чтобы "приближение" было к курсору
    const zoomingCenter = {
      x: mousePos.x,
      y: mousePos.y,
    };

    const deltaOffsetX = (zoomingCenter.x - center.value.x) * (deltaScale - 1);
    const deltaOffsetY = (zoomingCenter.y - center.value.y) * (deltaScale - 1);

    center.value = {
      x: center.value.x - deltaOffsetX,
      y: center.value.y - deltaOffsetY,
    };
  }
};

/* ===================== Логика соединения блоков (linking) ===================== */

/**
 * linkingStart:
 *   - начало "протягивания" связи от исходного блока/слота
 */
const linkingStart = (block: Block, slotNumber: number) => {
  linkStartData.value = { block, slotNumber };

  const linkStartPos = getConnectionPos(block, slotNumber, false);
  if (linkStartPos) {
    tempLink.value = {
      x1: linkStartPos.x,
      y1: linkStartPos.y,
      x2: mousePos.x,
      y2: mousePos.y,
      style: {
        stroke: '#8f8f8f',
        strokeWidth: 4 * scale.value,
        fill: 'none',
      },
    };
  }
  linking.value = true;
};

/**
 * linkingStop:
 *   - завершение "протягивания" при отпускании на целевом блоке
 *   - создаёт новую связь (если нет петли) и удаляет старые, если были
 */
const linkingStop = (targetBlock: Block) => {
  if (linkStartData.value && targetBlock) {
    const maxId = Math.max(0, ...links.value.map((l) => +l.id || 0));

    // Проверяем петли
    if (linkStartData.value.block.id === targetBlock.id) {
      console.error('Обнаружена петля! Ответ не может ссылаться сам на себя.');
    } else if (targetBlock.id === firstBlock.value?.id) {
      console.error('Обнаружена петля! Ответ подключен к первому блоку.');
    }
    // Если "checkbox" — проводим связь сразу для всех outputs
    else if (linkStartData.value.block.type === 'checkbox') {
      const findLinks = links.value.filter((v) => v.originId === linkStartData.value?.block?.id);
      if (findLinks.length) {
        findLinks.forEach((ln) => removeLink(ln.id));
      }
      // Все ответы ведут на один и тот же следующий блок
      linkStartData.value.block.outputs.forEach((_, i: number) => {
        links.value.push({
          id: maxId + 1,
          originId: linkStartData.value?.block?.id || 0,
          originSlot: i,
          targetId: targetBlock.id,
        });
      });
    } else {
      // Стандартная связь
      const existingLink = links.value.find(
        (l) =>
          l.originId === linkStartData.value!.block.id &&
          l.originSlot === linkStartData.value!.slotNumber,
      );
      if (existingLink) {
        removeLink(existingLink.id);
      }
      links.value.push({
        id: maxId + 1,
        originId: linkStartData.value.block.id,
        originSlot: linkStartData.value.slotNumber,
        targetId: targetBlock.id,
      });
    }

    // Запоминаем "первый" блок, если он ещё не задан
    if (!firstBlock.value && !linkStartData.value.block.inputs[0].active) {
      firstBlock.value = linkStartData.value.block;
    }
  }

  linking.value = false;
  tempLink.value = null;
  linkStartData.value = null;
};

/**
 * linkingBreakOrigin:
 *   - разрыв существующей связи от исходного блока/слота,
 *     затем начало новой связи от того же места
 */
const linkingBreakOrigin = (originBlock: Block, slotNumber: number) => {
  if (originBlock && slotNumber > -1) {
    if (originBlock.type === 'checkbox') {
      links.value = links.value.filter((l) => l.originId !== originBlock.id);
    } else {
      const found = links.value.find(
        (l) => l.originId === originBlock.id && l.originSlot === slotNumber,
      );
      if (found) {
        removeLink(found.id);
      }
    }
    linkingStart(originBlock, slotNumber);
  }
};

/**
 * linkingBreak:
 *   - разрыв существующей связи от целевого блока,
 *     затем начало новой связи от блока-источника
 */
const linkingBreak = (targetBlock: Block) => {
  if (targetBlock) {
    const foundLink = links.value.find((l) => l.targetId === targetBlock.id);
    if (foundLink) {
      const originBlock = blocks.value.find((b) => b.id === foundLink.originId);
      removeLink(foundLink.id);
      if (originBlock) {
        linkingStart(originBlock, foundLink.originSlot);
      }
    }
  }
};

/**
 * findFirstBlock:
 *   - ищет первый блок (не имеет входящих связей, но имеет выходящие)
 */
const findFirstBlock = (blocksArr: Block[]) => {
  return (
    blocksArr.find(
      (block) =>
        block.inputs.every((input) => !input.active) &&
        block.outputs.some((output) => output.active),
    ) ?? null
  );
};

/**
 * updateContainer:
 *   - подтягиваем данные по контейнеру из кэша
 */
const updateContainer = () => {
  const rawContainerData = localStorage.getItem('container');

  if (rawContainerData) {
    container.value = JSON.parse(rawContainerData);
  }
};

/* ===================== Жизненный цикл компонента ===================== */
onMounted(() => {
  // Проверяем данные по контейнеру в localStorage
  updateContainer();

  // При первом рендере выставляем центр, если он не задан
  if (containerElement.value && (!center.value.x || !center.value.y)) {
    center.value = {
      x: 24,
      y: containerElement.value.clientHeight / 2,
    };
  }

  // Глобальные слушатели для мыши и колёсика
  document.documentElement.addEventListener('mousemove', handleMove, true);
  document.documentElement.addEventListener('mousedown', handleDown, true);
  document.documentElement.addEventListener('mouseup', handleUp, true);

  // Ищем "первый" блок при инициализации
  firstBlock.value = findFirstBlock(blocks.value);
});

onBeforeUnmount(() => {
  // Убираем слушатели при удалении компонента
  document.documentElement.removeEventListener('mousemove', handleMove, true);
  document.documentElement.removeEventListener('mousedown', handleDown, true);
  document.documentElement.removeEventListener('mouseup', handleUp, true);
});

watch(
  container,
  debounce((val) => {
    localStorage.setItem('container', JSON.stringify(val));
  }),
  { deep: true },
);

/** Следим за списком links: при изменении пересчитываем активные слоты */
watch(
  links,
  (newVal) => {
    prepareBlocksLinking(blocks.value, newVal);

    // Если связей нет, сбрасываем "первый" блок
    if (!newVal?.length && firstBlock.value) {
      firstBlock.value = null;
    }
  },
  { immediate: true, deep: true },
);
</script>

<template>
  <div class="logics-blocks-container" ref="containerElement" @wheel.prevent="handleWheel">
    <LogicsLinks class="logics-blocks-container__links" :lines="lines" />
    <LogicsBlock
      v-for="block in blocks"
      :key="block.id"
      v-bind="block"
      v-model:x="block.x"
      v-model:y="block.y"
      :selected="isSelectedBlock(block)"
      :options="optionsForChild"
      @linkingStart="linkingStart(block, $event)"
      @linkingStop="linkingStop(block)"
      @linkingBreak="linkingBreak(block)"
      @linkingBreakOrigin="linkingBreakOrigin(block, $event)"
      @select="blockSelect(block)"
    />
  </div>
</template>

<style lang="scss" scoped>
.logics-blocks-container {
  position: relative;
  overflow: hidden;
  box-sizing: border-box;
  width: 100%;
  height: 100%;

  &__links {
    position: relative;
    z-index: 5;
  }
}
</style>
