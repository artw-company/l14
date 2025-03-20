import { getOffsetRect } from './dom.ts';

export const getMousePosition = (element: HTMLElement, event: MouseEvent) => {
  const mouseX = event.pageX || event.clientX + document.documentElement.scrollLeft;
  const mouseY = event.pageY || event.clientY + document.documentElement.scrollTop;

  const offset = getOffsetRect(element);
  const x = mouseX - offset.left;
  const y = mouseY - offset.top;

  return {
    x: x,
    y: y,
  };
};
