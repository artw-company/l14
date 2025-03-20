from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import ValidationError

from ..models import Answer, QuestionAnswer, Survey
from ..serializers import SurveySerializer


class UpdateSurveyCommand:

    def __init__(
        self,
        survey_model: type[Survey],
        survey_serializer: type[SurveySerializer],
        answer_model: type[Answer],
        question_answer_model: type[QuestionAnswer],
    ):
        self.survey_model: type[Survey] = survey_model
        self.survey_serializer: type[SurveySerializer] = survey_serializer
        self.answer_model: type[Answer] = answer_model
        self.question_answer_model: type[QuestionAnswer] = question_answer_model

    def __call__(self, survey_id: int, data: dict | list[dict]) -> tuple[dict, int]:
        """
        Метод обновляет тексты вопросов и ответов и связи между ними в БД и возвращает обновленные данные
        Args:
            survey_id(int): чаcть URL запроса
            data(dict | list[dict]): данные запроса

        Returns:
            tuple[dict, int]: Кортеж из сериализованных данных и статуса ответа
        """
        survey: Survey | None = self.survey_model.objects.filter(id=survey_id).first()
        if not survey:
            return {"detail": "Опрос не найден."}, status.HTTP_404_NOT_FOUND

        questions_data: list | dict = data.get("questions", []) if isinstance(data, dict) else data
        if not questions_data:
            self._update_survey_name(survey, data)
            serializer = self.survey_serializer(survey)

            return serializer.data, status.HTTP_200_OK

        try:
            with transaction.atomic():
                self._update_survey_name(survey, data)
                self._update_questions(survey, questions_data)
                self._update_answers_and_links(survey, questions_data)
                serializer = self.survey_serializer(survey)
                return serializer.data, status.HTTP_200_OK

        except ValidationError as e:
            return {"detail": str(e)}, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            return {"detail": f"Произошла ошибка: {str(e)}"}, status.HTTP_500_INTERNAL_SERVER_ERROR

    def _update_survey_name(self, survey: Survey, data: dict) -> None:
        """
        Метод обновляет название опроса
        Args:
            survey(Survey) - oбъект модели Опрос
            data(dict) - данные запроса
        Returns:
            None
        """
        if "name" in data:
            survey.name = data["name"]
            survey.save()

    def _update_questions(self, survey: Survey, questions_data: list[dict]) -> None:
        """
        Метод обновляет текст вопросов
        Args:
            survey(Survey) - oбъект модели Опрос
            questions_data(list[dict]) - список объектов вопросов
        Returns:
            None
        """
        existing_questions = {q.id: q for q in survey.questions.all()}

        for question_data in questions_data:
            question_id = question_data.get("id")
            if not question_id or question_id not in existing_questions:
                raise ValidationError(f"Вопрос с id={question_id} не найден в текущем опросе.")

            if not all(k in question_data for k in ["id", "text", "short_text", "type"]):
                raise ValidationError(f"Отсутствуют обязательные поля в данных вопроса с id={question_id}")

            question = existing_questions[question_id]
            question.text = question_data["text"]
            question.short_text = question_data["short_text"]
            question.q_type = question_data["type"]
            question.meta = question_data.get("meta", question.meta)
            question.save()

    def _update_answers_and_links(self, survey: Survey, questions_data: list[dict]) -> None:
        """
        Метод обновляет текст ответов
        Args:
            survey(Survey) - oбъект модели Опрос
            questions_data(list[dict]) - список объектов вопросов
        Returns:
            None
        """
        existing_questions = {q.id: q for q in survey.questions.all()}
        existing_answers = {a.id: a for a in Answer.objects.filter(question_answers__question__survey=survey)}
        existing_qas = {
            (qa.question.id, qa.answer.id): qa
            for qa in self.question_answer_model.objects.filter(question__survey=survey)
        }

        for question_data in questions_data:
            question_id = question_data["id"]
            answers_data = question_data.get("answers", [])

            for answer_data in answers_data:
                if not all(k in answer_data for k in ["id", "text", "question_id"]):
                    raise ValidationError(f"Отсутствуют обязательные поля в данных ответа для вопроса id={question_id}")

                answer_id = answer_data["id"]
                if answer_id not in existing_answers:
                    raise ValidationError(f"Ответ с id={answer_id} не найден.")

                if answer_data["question_id"] != question_id:
                    raise ValidationError(
                        f"question_id {answer_data['question_id']} не соответствует ID вопроса {question_id}"
                    )

                # Обновляем Answer
                answer = existing_answers[answer_id]
                answer.text = answer_data["text"]
                answer.sort = answer_data.get("sort", answer.sort)
                answer.save()

                # Обновляем связь QuestionAnswer
                qa_key = (question_id, answer_id)
                if qa_key not in existing_qas:
                    raise ValidationError(f"Связь для вопроса id={question_id} и ответа id={answer_id} не найдена.")

                qa = existing_qas[qa_key]
                next_question_id = answer_data.get("next_question_id")
                if next_question_id is not None and next_question_id not in existing_questions:
                    raise ValidationError(f"Следующий вопрос с id={next_question_id} не найден в опросе.")

                qa.next_question = existing_questions.get(next_question_id) if next_question_id else None
                qa.save()
