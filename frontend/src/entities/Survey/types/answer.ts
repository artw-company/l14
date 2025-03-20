import type { Question } from './question.ts';

export interface Answer {
  id: number;
  text: string;
  sort: number;
  question_id: Question['id'];
  next_question_id: number | null;
}
