from flask import render_template, Blueprint
from flask.views import MethodView

from services.quiz_service import get_all_questions

# 루트 경로는 api/version 연결 x
home_bp = Blueprint("home_bp", __name__)

@home_bp.route("/")
def index():
    return render_template("index.html", swagger_url="/api/v1/swagger", quiz_table_url="/quiz-table")

@home_bp.route("/health-check")
def health_check():
    return "OK", 200

# @home_bp.route("/quiz-table")
# def quiz_table():
#     return render_template("quiz_table.html")

class QuizListResource(MethodView):
    def get(self):
        questions = get_all_questions()
        return render_template("quiz_table.html", questions=questions)

# as_view()를 사용해서 뷰 함수를 생성하고 blueprint에 등록
home_bp.add_url_rule('/quiz-table', view_func=QuizListResource.as_view('quiz_table'))