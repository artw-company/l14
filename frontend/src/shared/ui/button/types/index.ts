export interface ButtonProps {
  /**
   * Цветовая схема
   *
   * @default 'primary'
   */
  size?: 'sm' | 'md';

  /**
   * Цветовая схема
   *
   * @default 'primary'
   */
  theme?: 'primary' | 'secondary' | 'secondary-black';

  /**
   * Имя иконки, которая размещается правее текста кнопки.
   *
   * @default null
   */
  icon?: string | null;

  /**
   * Неактивное состояние кнопки.
   *
   * @default false
   */
  disabled?: boolean;

  /**
   * Состояние загрузки кнопки.
   *
   * @default false
   */
  loading?: boolean;

  /**
   * Включить активное состояние кнопки.
   *
   * @default false
   */
  active?: boolean;
}
