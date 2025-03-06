from flask_restx import Resource, reqparse, abort
from services.profile02_service import generate_profile

profile_parser = reqparse.RequestParser()
for i in range(5, 19):  # 닉네임, 결혼조건 생성에는 5번부터 18번까지의 질문만 사용
    profile_parser.add_argument(f"q{i}", type=int, required=True, help=f"Question {i} answer index cannot be blank")

class ProfileController(Resource):
    @classmethod
    def post(cls):
        args = profile_parser.parse_args()
        answer_indices = [args[f'q{i}'] for i in range(5, 19)]

        try:
            profile = generate_profile(answer_indices)
            return profile, 200
        except ValueError as ve:
            abort(400, "400-04: 응답이 존재하지 않습니다")  # 400-04: 응답이 존재하지 않습니다
        except Exception as e:
            abort(500, str(e))