from models.quiz_models import QuizQuestion


def get_all_questions():
    questions = QuizQuestion.query.all()

    # JSON 변환
    return [
        {
            "id": q.id,
            "type": q.type,
            "question": q.question,
            "options": [option.option_text for option in q.options]
        }
        for q in questions
    ]