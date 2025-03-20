import type { Question } from '@/entities/Survey';

export interface BlockSlot {
  id: number;
  name: string;
  label: string;
  active?: boolean;
}

export interface Block extends Pick<Question, 'id' | 'type'> {
  title: string;
  x: number;
  y: number;
  inputs: BlockSlot[];
  outputs: BlockSlot[];
}
