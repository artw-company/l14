from rest_framework import serializers

from .models import Answer, Question, QuestionAnswer, Survey


class QuestionAnswerSerializer(serializers.ModelSerializer):
    next_question_id = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(), source="next_question", allow_null=True, required=False
    )
    answer_id = serializers.PrimaryKeyRelatedField(queryset=Answer.objects.all(), source="answer", required=True)
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), allow_null=True, required=False)
    id = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = QuestionAnswer
        fields = ["id", "question", "answer_id", "next_question_id"]


class AnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, required=False)
    question_id = serializers.SerializerMethodField()
    next_question_id = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ["id", "text", "sort", "question_id", "next_question_id"]

    def get_question_id(self, obj):
        question_answer = obj.question_answers.first()
        return question_answer.question.id if question_answer and question_answer.question else None

    def get_next_question_id(self, obj):
        question_answer = obj.question_answers.first()
        return question_answer.next_question.id if question_answer and question_answer.next_question else None


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    type = serializers.CharField(source="q_type")

    class Meta:
        model = Question
        fields = ["id", "text", "short_text", "type", "meta", "answers"]

    def get_answers(self, obj: Question) -> list:
        """
        Получает все ответы, связанные с вопросом через QuestionAnswer.
        """
        answers = [qa.answer for qa in obj.question_answers.all()]
        return AnswerSerializer(answers, many=True).data


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    id = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Survey
        fields = ["id", "name", "questions"]
        read_only_fields = ["id"]
