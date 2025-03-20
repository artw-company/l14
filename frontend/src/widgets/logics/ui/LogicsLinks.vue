<script setup lang="ts">
import { computed } from 'vue';
import type { LineData } from '../types';

/**
 * Пропсы компонента:
 * - lines — массив линий
 * - outline — включать ли рисование подложки (outline)
 */
const props = defineProps<{
  lines?: LineData[];
  outline?: boolean;
}>();

/**
 * Функция вычисления расстояния между двумя точками (x1, y1) и (x2, y2).
 */
const distance = (x1: number, y1: number, x2: number, y2: number): number => {
  return Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
};

/**
 * Вычисление промежуточной точки на кубической кривой Безье
 * для обеспечения плавного перехода (используется для стрелок).
 */
const computeConnectionPoint = (
  x1: number,
  y1: number,
  x2: number,
  y2: number,
  t: number,
): { x: number; y: number } => {
  const dist = distance(x1, y1, x2, y2);
  const p0 = { x: x1, y: y1 };
  const p1 = { x: x1 + dist * 0.25, y: y1 };
  const p2 = { x: x2 - dist * 0.25, y: y2 };
  const p3 = { x: x2, y: y2 };

  const c1 = (1 - t) * (1 - t) * (1 - t);
  const c2 = 3 * (1 - t) * (1 - t) * t;
  const c3 = 3 * (1 - t) * (t * t);
  const c4 = t * t * t;

  const x = c1 * p0.x + c2 * p1.x + c3 * p2.x + c4 * p3.x;
  const y = c1 * p0.y + c2 * p1.y + c3 * p2.y + c4 * p3.y;
  return { x, y };
};

/**
 * Вычисление массивов данных для отрисовки самих кривых.
 */
const renderedPathes = computed(() => {
  if (!props.lines) {
    return [];
  }
  return props.lines.map((line) => {
    const dist = distance(line.x1, line.y1, line.x2, line.y2) * 0.25;
    return {
      data: `M ${line.x1}, ${line.y1} C ${line.x1 + dist}, ${line.y1}, ${
        line.x2 - dist
      }, ${line.y2}, ${line.x2}, ${line.y2}`,
      style: line.style,
      outlineStyle: line.outlineStyle,
    };
  });
});

/**
 * Вычисление массивов данных для отрисовки стрелок.
 */
const renderedArrows = computed(() => {
  if (!props.lines) {
    return [];
  }

  return props.lines.map((line) => {
    // Берём центральную точку (t=0.5)
    const pos = computeConnectionPoint(line.x1, line.y1, line.x2, line.y2, 0.5);
    // Берём точку чуть дальше (t=0.51), чтобы вычислить угол наклона
    const pos2 = computeConnectionPoint(line.x1, line.y1, line.x2, line.y2, 0.51);

    const angle = -Math.atan2(pos2.x - pos.x, pos2.y - pos.y);
    const degrees = ((angle >= 0 ? angle : 2 * Math.PI + angle) * 180) / Math.PI;

    return {
      transform: `translate(${pos.x}, ${pos.y}) rotate(${degrees})`,
      style: {
        stroke: line.style?.stroke,
        strokeWidth: line.style?.strokeWidth ? line.style.strokeWidth * 2 : 0,
        fill: line.style?.stroke,
        opacity: line.style?.opacity,
      },
    };
  });
});
</script>

<template>
  <svg class="logics-links" width="100%" height="100%">
    <g v-for="(path, index) in renderedPathes" :key="index">
      <path v-if="outline" :d="path.data" :style="path.outlineStyle"></path>
      <path :d="path.data" :style="path.style"></path>
    </g>
    <g>
      <path
        v-for="(arrow, index) in renderedArrows"
        :key="index"
        d="M -1 -1 L 0 1 L 1 -1 z"
        :style="arrow.style"
        :transform="arrow.transform"
      ></path>
    </g>
  </svg>
</template>

<style scoped>
.logics-links {
  pointer-events: none;
}
</style>
