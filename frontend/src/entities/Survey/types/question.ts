import type { Answer } from './answer.ts';

export type QuestionTypes = 'radio' | 'checkbox';

export interface QuestionPosition {
  x: number;
  y: number;
}

export interface Question {
  id: number;
  text: string;
  short_text: string;
  type: QuestionTypes;
  meta: {
    position: QuestionPosition;
  };
  answers: Answer[];
}
