from flask import render_template
from flask_restx import Resource, reqparse, abort
from services.quiz_service import get_all_questions

quiz_parser = reqparse.RequestParser()
quiz_parser.add_argument(
    "include_options",
    type=bool,
    required=False,
    default=True,
    help="선택지를 포함할지 여부 (기본값: True)"
)

class QuizQuestionsController(Resource):
    def get(self):
        try:
            questions = get_all_questions()
            return {"questions": questions}, 200
        except ValueError:
            abort(400, "400-03: 테이블에 데이터가 없습니다")  # 400-03: 테이블에 데이터가 없습니다
        except Exception as e:
            abort(500, "500-00: 서버 내부 오류가 발생했습니다")  # 500-00: 서버 내부 오류가 발생했습니다

class QuizListController(Resource):
    def get(self):
        questions = get_all_questions()
        return render_template("quiz_table.html", questions=questions)