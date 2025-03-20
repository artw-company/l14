from django.db import migrations


def populate_data(apps, schema_editor):
    Survey = apps.get_model("survey", "Survey")
    Question = apps.get_model("survey", "Question")
    QuestionAnswer = apps.get_model("survey", "QuestionAnswer")
    Answer = apps.get_model("survey", "Answer")

    survey_data = [
        {
            "id": 55,
            "text": "Сколько вам лет?",
            "short_text": "Возрастная категория",
            "type": "radio",
            "meta": {"position": {"x": 300, "y": 0}},
            "answers": [
                {"id": 158, "text": "До 18", "sort": 1, "next_question_id": 56},
                {"id": 159, "text": "От 18 до 60", "sort": 2, "next_question_id": 56},
                {"id": 160, "text": "Старше 60", "sort": 3, "next_question_id": 57},
            ],
        },
        {
            "id": 61,
            "text": "Какой вид транспорта предпочитаете?",
            "short_text": "Транспорт",
            "type": "checkbox",
            "meta": {"position": {"x": 1800, "y": -150}},
            "answers": [
                {"id": 176, "text": "Самолет", "sort": 4, "next_question_id": 63},
                {"id": 177, "text": "Поезд", "sort": 5, "next_question_id": 63},
                {"id": 178, "text": "Автомобиль", "sort": 6, "next_question_id": 63},
            ],
        },
        {
            "id": 59,
            "text": "На какой срок планируете поездку?",
            "short_text": "Длительность",
            "type": "checkbox",
            "meta": {"position": {"x": 1200, "y": 0}},
            "answers": [
                {"id": 170, "text": "До недели", "sort": 7, "next_question_id": 60},
                {"id": 171, "text": "От недели до двух", "sort": 8, "next_question_id": 60},
                {"id": 172, "text": "Больше двух недель", "sort": 9, "next_question_id": 60},
            ],
        },
        {
            "id": 60,
            "text": "Нужны ли вам дополнительные сервисы?",
            "short_text": "Доп. услуги",
            "type": "radio",
            "meta": {"position": {"x": 1500, "y": 0}},
            "answers": [
                {"id": 173, "text": "Трансфер из аэропорта", "sort": 10, "next_question_id": 61},
                {"id": 174, "text": "Детские программы", "sort": 11, "next_question_id": 62},
                {"id": 175, "text": "Ничего не нужно", "sort": 12, "next_question_id": 62},
            ],
        },
        {
            "id": 62,
            "text": "Хотели бы вы эксклюзивные экскурсии?",
            "short_text": "Экскурсии",
            "type": "checkbox",
            "meta": {"position": {"x": 1800, "y": 150}},
            "answers": [
                {"id": 179, "text": "Да", "sort": 13, "next_question_id": 63},
                {"id": 180, "text": "Нет", "sort": 14, "next_question_id": 63},
                {"id": 181, "text": "Подумаю", "sort": 15, "next_question_id": 63},
            ],
        },
        {
            "id": 58,
            "text": "Какой у вас примерный бюджет?",
            "short_text": "Финансы",
            "type": "checkbox",
            "meta": {"position": {"x": 900, "y": 0}},
            "answers": [
                {"id": 167, "text": "До 50 000 руб.", "sort": 16, "next_question_id": 59},
                {"id": 168, "text": "От 50 000 до 100 000 руб.", "sort": 17, "next_question_id": 59},
                {"id": 169, "text": "Свыше 100 000 руб.", "sort": 18, "next_question_id": 59},
            ],
        },
        {
            "id": 56,
            "text": "Что для вас важнее всего в путешествии?",
            "short_text": "Приоритеты",
            "type": "checkbox",
            "meta": {"position": {"x": 600, "y": -150}},
            "answers": [
                {"id": 161, "text": "Комфорт", "sort": 19, "next_question_id": 58},
                {"id": 162, "text": "Экономия", "sort": 20, "next_question_id": 58},
                {"id": 163, "text": "Новые впечатления", "sort": 21, "next_question_id": 58},
            ],
        },
        {
            "id": 57,
            "text": "В какой сезон вы предпочитаете путешествовать?",
            "short_text": "Сезонность",
            "type": "checkbox",
            "meta": {"position": {"x": 600, "y": 150}},
            "answers": [
                {"id": 164, "text": "Лето", "sort": 22, "next_question_id": 58},
                {"id": 165, "text": "Зима", "sort": 23, "next_question_id": 58},
                {"id": 166, "text": "В любое время", "sort": 24, "next_question_id": 58},
            ],
        },
        {
            "id": 54,
            "text": "Для какой цели вы планируете поездку?",
            "short_text": "Общие сведения",
            "type": "checkbox",
            "meta": {"position": {"x": 0, "y": 0}},
            "answers": [
                {"id": 155, "text": "Отпуск", "sort": 25, "next_question_id": 55},
                {"id": 156, "text": "Командировка", "sort": 26, "next_question_id": 55},
                {"id": 157, "text": "Путешествие с семьей", "sort": 27, "next_question_id": 55},
            ],
        },
        {
            "id": 63,
            "text": "Нужны ли вам дополнительные льготы?",
            "short_text": "Льготы",
            "type": "checkbox",
            "meta": {"position": {"x": 2100, "y": 0}},
            "answers": [
                {"id": 182, "text": "Студенческие", "sort": 28, "next_question_id": None},
                {"id": 183, "text": "Ветеранам труда", "sort": 29, "next_question_id": None},
                {"id": 184, "text": "По инвалидности", "sort": 30, "next_question_id": None},
            ],
        },
    ]

    survey = Survey.objects.create(name="Основной опрос")

    questions_by_id = {}

    for question_data in survey_data:
        question = Question.objects.create(
            survey=survey,
            id=question_data["id"],
            text=question_data["text"],
            short_text=question_data["short_text"],
            q_type=question_data["type"],
            meta=question_data["meta"],
        )
        questions_by_id[question.id] = question

    # Создаем ответы и связи QuestionAnswer
    for question_data in survey_data:
        question = questions_by_id[question_data["id"]]
        for answer_data in question_data["answers"]:
            answer = Answer.objects.create(id=answer_data["id"], text=answer_data["text"], sort=answer_data["sort"])
            next_question = (
                questions_by_id.get(answer_data["next_question_id"])
                if answer_data["next_question_id"] is not None
                else None
            )
            QuestionAnswer.objects.create(question=question, answer=answer, next_question=next_question)


def reverse_populate_data(apps, schema_editor):
    Survey = apps.get_model("survey", "Survey")
    Question = apps.get_model("survey", "Question")
    QuestionAnswer = apps.get_model("survey", "QuestionAnswer")
    Answer = apps.get_model("survey", "Answer")

    QuestionAnswer.objects.all().delete()
    Answer.objects.all().delete()
    Question.objects.all().delete()
    Survey.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("survey", "0001_initial"),  # Убедитесь, что это правильная зависимость
    ]

    operations = [
        migrations.RunPython(populate_data, reverse_code=reverse_populate_data),
    ]
