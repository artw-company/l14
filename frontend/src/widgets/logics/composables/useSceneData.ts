import type { Question, Answer } from '@/entities/Survey';
import type { Link, Block } from '../types';
import { ref, type ShallowRef, watch } from 'vue';
import deepmerge from 'deepmerge';

export const useSceneData = (questions: ShallowRef<Question[]>) => {
  const blocks = ref<Block[]>([]);
  const links = ref<Link[]>([]);

  //region Подготовка блоков

  const createOutputsFromAnswers = (answers: Answer[]) => {
    return answers.map(({ text, id }) => ({
      id: id,
      name: text,
      label: text,
    }));
  };

  const createBlock = (question: Question): Block => {
    const { id, type, text, short_text, answers, meta } = question;
    const { x, y } = meta.position;

    // формируем outputs из answers
    const outputs = createOutputsFromAnswers(answers);
    const inputs = [
      {
        id,
        name: type,
        label: short_text || type,
        active: false,
      },
    ];

    return {
      id,
      title: text || short_text,
      type,
      x,
      y,
      inputs,
      outputs,
    };
  };

  const prepareBlocks = (blocksArr: Question[]): Block[] => {
    return blocksArr.map((block) => createBlock(block));
  };
  //endregion

  //region Подготовка связей

  const prepareLinks = (questions: Question[]) => {
    let linkIndex = 0;

    return questions.reduce((res: Link[], question) => {
      question.answers.forEach((answer, index) => {
        if (!answer.next_question_id) {
          return;
        }

        res.push({
          id: linkIndex,
          originId: question.id,
          originSlot: index,
          targetId: answer.next_question_id,
        });

        linkIndex += 1;
      });

      return res;
    }, []);
  };
  //endregion

  const exportOriginData = (): Question[] => {
    const clonedQuestions = deepmerge([], questions.value);

    const blocksDictionary = blocks.value.reduce(
      (res, block) => {
        res[block.id] = block;
        return res;
      },
      {} as Record<number, Block>,
    );

    const answerTargetsDictionary = links.value.reduce(
      (res, link) => {
        res[`${link.originId}_${link.originSlot}`] = link.targetId;
        return res;
      },
      {} as Record<string, number>,
    );

    return clonedQuestions.map((question) => {
      const currentBlock = blocksDictionary[question.id];
      question.meta.position = { x: currentBlock.x, y: currentBlock.y };

      for (const index in question.answers) {
        question.answers[index].next_question_id =
          answerTargetsDictionary[`${question.id}_${index}`] ?? null;
      }

      return question;
    });
  };

  watch(
    questions,
    (val) => {
      links.value = prepareLinks(val);
      blocks.value = prepareBlocks(val);
    },
    { immediate: true },
  );

  return {
    blocks,
    links,
    exportOriginData,
  };
};
