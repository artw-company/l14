import pytest
from django.test import TestCase
from survey.models import Answer, Question, QuestionAnswer, Survey
from survey.serializers import AnswerSerializer, QuestionSerializer, SurveySerializer


@pytest.mark.django_db
class TestSerializers(TestCase):
    def setUp(self):
        self.survey = Survey.objects.create(name="Простой опрос")  # Без id
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

    def test_answer_serializer(self):
        serializer = AnswerSerializer(self.a1)
        data = serializer.data
        assert data["text"] == "Да"
        assert data["sort"] == 0
        assert data["question_id"] == self.q1.id
        assert data["next_question_id"] == self.q2.id

    def test_question_serializer(self):
        serializer = QuestionSerializer(self.q1)
        data = serializer.data
        assert data["text"] == "Вы любите путешествия?"
        assert data["short_text"] == "Путешествия"
        assert data["q_type"] == "radio"
        assert data["meta"] == {}
        assert len(data["answers"]) == 2
        assert data["answers"][0]["text"] == "Да"

    def test_survey_serializer(self):
        serializer = SurveySerializer(self.survey)
        data = serializer.data
        assert data["name"] == "Простой опрос"
        assert len(data["questions"]) == 2
        assert data["questions"][0]["text"] == "Вы любите путешествия?"
