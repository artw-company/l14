from rest_framework import status

from ..models import Survey
from ..serializers import SurveySerializer


class GetSurveyQuestionsQuery:

    def __init__(self, survey_model: type[Survey], survey_serializer: type[SurveySerializer]):
        self.survey_model: type[Survey] = survey_model
        self.survey_serializer: type[SurveySerializer] = survey_serializer

    def __call__(self, survey_id: int) -> tuple[dict, int]:
        """
        Получает список вопросов для указанного опроса.

        :param survey_id: ID опроса.
        :return: Кортеж из данных опроса (с вопросами, ответами и связями) и HTTP-статуса.
        """

        survey: Survey | None = self.survey_model.objects.filter(id=survey_id).first()

        if survey is None:
            return {"detail": "Опрос не найден."}, status.HTTP_404_NOT_FOUND

        serializer: SurveySerializer = self.survey_serializer(survey)

        return serializer.data, status.HTTP_200_OK
