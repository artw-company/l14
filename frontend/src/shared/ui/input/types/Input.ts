export interface InputIconItem {
  name: string;
  clickable?: boolean;
}

export type InputType =
  | 'button'
  | 'checkbox'
  | 'color'
  | 'date'
  | 'datetime-local'
  | 'email'
  | 'file'
  | 'hidden'
  | 'image'
  | 'month'
  | 'number'
  | 'password'
  | 'radio'
  | 'range'
  | 'reset'
  | 'search'
  | 'submit'
  | 'tel'
  | 'text'
  | 'time'
  | 'url'
  | 'week';

export interface InputProps {
  /**
   * Имя элемента формы.
   */
  name: string;

  /**
   * Значение для пустого поля.
   *
   * @default ''
   */
  placeholder?: string;

  /**
   * Состояние отключения элемента.
   *
   * @default false
   */
  disabled?: boolean;

  /**
   * Состояние только для чтения.
   *
   * @default false
   */
  readonly?: boolean;

  /**
   * Значение модели.
   */
  modelValue: string;

  /**
   * Тип элемента формы.
   *
   * @default 'text'
   */
  type?: InputType;

  /**
   * Иконка в начале инпута.
   *
   * @default undefined
   */
  prependIcon?: InputIconItem;

  /**
   * Иконка в конце инпута.
   *
   * @default undefined
   */
  appendIcon?: InputIconItem;
}
