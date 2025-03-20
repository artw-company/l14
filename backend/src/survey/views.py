from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response

from .commands.update_survey import UpdateSurveyCommand
from .models import Answer, QuestionAnswer, Survey
from .queries.get_survey_questions import GetSurveyQuestionsQuery
from .serializers import QuestionSerializer, SurveySerializer


class SurveyDetailView(generics.RetrieveUpdateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    lookup_field = "id"

    @extend_schema(
        summary="Получение объекта запроса",
        description="""Возвращает объект запроса по id с вопросами, ответами и актуальными связями между ними
         для отображения на фронте""",
        responses={200: QuestionSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        survey_id = kwargs.get("id")
        get_survey_questions_query = GetSurveyQuestionsQuery(survey_model=Survey, survey_serializer=SurveySerializer)
        result, status_code = get_survey_questions_query(survey_id)
        return Response(result, status=status_code)

    @extend_schema(
        summary="Обновление связи и текстов вопросов и ответов по id опроса",
        description="""Обновляет связи и текст вопросов и ответов по id опроса""",
        responses={200: SurveySerializer},
        request=SurveySerializer,
    )
    def put(self, request, *args, **kwargs):
        survey_id = kwargs.get("id")
        data = request.data
        update_survey_command: UpdateSurveyCommand = UpdateSurveyCommand(
            survey_model=Survey,
            survey_serializer=SurveySerializer,
            answer_model=Answer,
            question_answer_model=QuestionAnswer,
        )
        result, status_code = update_survey_command(survey_id, data)
        return Response(result, status=status_code)

    @extend_schema(exclude=True)
    def patch(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
