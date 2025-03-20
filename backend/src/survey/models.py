from django.db import models


class Survey(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название опроса")
    sort = models.IntegerField(default=0, verbose_name="Порядок сортировки")

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    def __str__(self):
        return self.name


class Question(models.Model):
    TYPE_CHOICES = (
        ("radio", "Radio"),
        ("checkbox", "Checkbox"),
    )

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions", verbose_name="Опрос")
    text = models.TextField(verbose_name="Текст вопроса")
    short_text = models.CharField(max_length=255, verbose_name="Короткий текст вопроса")
    q_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип вопроса")
    meta = models.JSONField(default=dict, verbose_name="Метаданные")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=255, verbose_name="Текст ответа")
    sort = models.IntegerField(default=0, verbose_name="Порядок сортировки")

    class Meta:
        ordering = ["sort"]
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.text


class QuestionAnswer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="question_answers", verbose_name="Вопрос", unique=False
    )
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="question_answers", verbose_name="Ответ")
    next_question = models.ForeignKey(
        Question,
        on_delete=models.SET_NULL,
        related_name="next_question_answers",
        null=True,
        blank=True,
        verbose_name="Следующий вопрос",
        unique=False,
    )

    class Meta:
        verbose_name = "Связь вопроса и следующего вопроса"
        verbose_name_plural = "Связи вопросов и следующих вопросов"
        unique_together = ("question", "answer")

    def __str__(self):
        return (
            f"{self.question.text} -> {self.answer.text} -> {self.next_question.text if self.next_question else 'None'}"
        )
