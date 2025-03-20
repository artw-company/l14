import json
from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from survey.models import Answer, Question, QuestionAnswer, Survey
from survey.serializers import QuestionSerializer, SurveySerializer


@pytest.mark.django_db
class TestSurveyDetailView:
    def setup_method(self):
        self.client = APIClient()
        self.survey = Survey.objects.create(name="Простой опрос")
        self.q1 = Question.objects.create(
            survey=self.survey, text="Вы любите путешествия?", short_text="Путешествия", q_type="radio", meta={}
        )
        self.q2 = Question.objects.create(
            survey=self.survey, text="Какой транспорт предпочитаете?", short_text="Транспорт", q_type="radio", meta={}
        )
        self.a1 = Answer.objects.create(text="Да", sort=0)
        self.a2 = Answer.objects.create(text="Нет", sort=1)
        self.a3 = Answer.objects.create(text="Самолет", sort=0)
        self.a4 = Answer.objects.create(text="Поезд", sort=1)
        QuestionAnswer.objects.create(question=self.q1, answer=self.a1, next_question=self.q2)
        QuestionAnswer.objects.create(question=self.q1, answer=self.a2, next_question=None)
        QuestionAnswer.objects.create(question=self.q2, answer=self.a3, next_question=None)
        QuestionAnswer.objects.create(question=self.q2, answer=self.a4, next_question=None)

    @patch("survey.views.GetSurveyQuestionsQuery")
    def test_get_survey(self, MockQuery):
        MockQuery.return_value.return_value = (
            QuestionSerializer([self.q1, self.q2], many=True).data,
            status.HTTP_200_OK,
        )
        url = reverse("survey-detail", kwargs={"id": self.survey.id})
        response = self.client.get(url, content_type="application/json")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        assert data[0]["id"] == self.q1.id
        assert data[0]["text"] == "Вы любите путешествия?"
        assert data[0]["answers"][0]["text"] == "Да"
        assert data[0]["answers"][0]["next_question_id"] == self.q2.id
        assert data[1]["id"] == self.q2.id
        assert data[1]["answers"][1]["text"] == "Поезд"

    @patch("survey.views.GetSurveyQuestionsQuery")
    def test_get_survey_not_found(self, MockQuery):
        # Мокаем ошибку 404
        MockQuery.return_value.return_value = ({"detail": "Опрос не найден."}, status.HTTP_404_NOT_FOUND)
        url = reverse("survey-detail", kwargs={"id": 999})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Опрос не найден."

    @patch("survey.views.UpdateSurveyCommand")
    def test_put_survey(self, MockCommand):
        updated_data = SurveySerializer(self.survey).data
        updated_data["name"] = "Обновленный опрос"
        updated_data["questions"][0]["text"] = "Вы любите путешествия? (новое)"
        updated_data["questions"][0]["answers"][0]["text"] = "Да, конечно"
        updated_data["questions"][0]["answers"][0]["next_question_id"] = None
        updated_data["questions"][1]["text"] = "Какой транспорт лучше?"
        updated_data["questions"][1]["answers"][0]["text"] = "Авиа"
        updated_data["questions"][1]["answers"][0]["next_question_id"] = self.q1.id
        MockCommand.return_value.return_value = (updated_data, status.HTTP_200_OK)

        url = reverse("survey-detail", kwargs={"id": self.survey.id})
        print("Generated URL:", url)  # Отладка URL
        request_data = {
            "id": self.survey.id,
            "name": "Обновленный опрос",
            "questions": [
                {
                    "id": self.q1.id,
                    "text": "Вы любите путешествия? (новое)",
                    "short_text": "Путешествия",
                    "q_type": "radio",
                    "meta": {"x": 10},
                    "answers": [
                        {"id": self.a1.id, "text": "Да, конечно", "question_id": self.q1.id, "next_question_id": None},
                        {
                            "id": self.a2.id,
                            "text": "Не очень",
                            "question_id": self.q1.id,
                            "next_question_id": self.q2.id,
                        },
                    ],
                },
                {
                    "id": self.q2.id,
                    "text": "Какой транспорт лучше?",
                    "short_text": "Транспорт",
                    "q_type": "radio",
                    "meta": {"y": 20},
                    "answers": [
                        {"id": self.a3.id, "text": "Авиа", "question_id": self.q2.id, "next_question_id": self.q1.id},
                        {"id": self.a4.id, "text": "Ж/Д", "question_id": self.q2.id, "next_question_id": None},
                    ],
                },
            ],
        }
        # Сериализуем request_data в JSON-строку
        response = self.client.put(url, data=json.dumps(request_data), content_type="application/json")
        if response.status_code != status.HTTP_200_OK:
            print("Response status:", response.status_code)
            print("Response content:", response.json())
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Обновленный опрос"
        assert data["questions"][0]["text"] == "Вы любите путешествия? (новое)"
        assert data["questions"][0]["answers"][0]["text"] == "Да, конечно"
        assert data["questions"][0]["answers"][0]["next_question_id"] is None
        assert data["questions"][1]["answers"][0]["text"] == "Авиа"
        assert data["questions"][1]["answers"][0]["next_question_id"] == self.q1.id

    @patch("survey.views.UpdateSurveyCommand")
    def test_put_survey_invalid_question_id(self, MockCommand):
        MockCommand.return_value.return_value = (
            {"detail": "Вопрос с id=999 не найден в опросе."},
            status.HTTP_400_BAD_REQUEST,
        )
        url = reverse("survey-detail", kwargs={"id": self.survey.id})
        invalid_data = {
            "id": self.survey.id,
            "name": "Обновленный опрос",
            "questions": [
                {
                    "id": 999,  # Несуществующий вопрос
                    "text": "Новый вопрос",
                    "short_text": "Новый",
                    "q_type": "radio",
                    "meta": {},
                    "answers": [{"id": self.a1.id, "text": "Да", "question_id": 999, "next_question_id": None}],
                }
            ],
        }
        response = self.client.put(url, invalid_data, content_type="application/json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch("survey.views.UpdateSurveyCommand")
    def test_put_survey_invalid_answer_id(self, MockCommand):
        MockCommand.return_value.return_value = ({"detail": "Ответ с id=999 не найден."}, status.HTTP_400_BAD_REQUEST)
        url = reverse("survey-detail", kwargs={"id": self.survey.id})
        invalid_data = {
            "id": self.survey.id,
            "name": "Обновленный опрос",
            "questions": [
                {
                    "id": self.q1.id,
                    "text": "Вы любите путешествия?",
                    "short_text": "Путешествия",
                    "q_type": "radio",
                    "meta": {},
                    "answers": [
                        {
                            "id": 999,
                            "text": "Да",
                            "question_id": self.q1.id,
                            "next_question_id": None,
                        }  # Несуществующий ответ
                    ],
                }
            ],
        }
        response = self.client.put(url, invalid_data, content_type="application/json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_patch_survey_not_allowed(self):
        url = reverse("survey-detail", kwargs={"id": self.survey.id})
        response = self.client.patch(url, {}, content_type="application/json")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
