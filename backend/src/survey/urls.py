from django.urls import path

from . import views

urlpatterns = [
    path("survey/<int:id>/", views.SurveyDetailView.as_view(), name="survey-detail"),
]
