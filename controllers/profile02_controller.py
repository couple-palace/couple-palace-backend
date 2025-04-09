from flask import request
from flask_restx import Resource, abort
from services.profile02_service import generate_profile


class ProfileController(Resource):
    def post(self):
        data = request.get_json(silent=True)
        if not data:
            abort(400, "400-04: JSON 본문이 필요합니다")

        if "questionsList" not in data or "job" not in data:
            abort(400, "400-06: 'questionsList'와 'job'을 모두 포함해야 합니다")

        questions_list = data["questionsList"]
        job = data["job"]

        if not isinstance(questions_list, list):
            abort(400, "400-08: questionsList는 리스트여야 합니다")

        for q in questions_list:
            if not isinstance(q, dict):
                abort(400, "400-05: 각 질문은 객체여야 합니다")
            for field in ("question_idx", "answer_idx", "type"):
                if field not in q:
                    abort(400, f"400-06: 각 질문은 '{field}'를 포함해야 합니다")
            try:
                int(q["question_idx"])
                int(q["answer_idx"])
            except ValueError:
                abort(400, "400-09: question_idx와 answer_idx는 정수여야 합니다")

        try:
            profile = generate_profile(questions_list, job)
            return profile, 200
        except ValueError:
            abort(400, "400-07: 프로필을 생성할 수 없습니다")
        except Exception:
            abort(500, "500-00: 서버 내부 오류가 발생했습니다")