from flask_restx import Resource, reqparse, abort
from services.profile02_service import generate_profile

# 요청 본문에서 q1 ~ q18 까지의 인자를 받도록 설정합니다.
profile_parser = reqparse.RequestParser()
for i in range(1, 19):
    profile_parser.add_argument(
        f"q{i}",
        type=int,
        required=True,
        help=f"질문 {i} 번에 대한 응답은 공백이 불가합니다"
    )

class ProfileController(Resource):
    def post(self):
        # 요청 파라미터(1~18번 질문)를 파싱합니다.
        args = profile_parser.parse_args()

        # 서비스에는 기존과 같이 5번부터 18번까지의 응답 인덱스만 전달합니다.
        answer_indices = [args[f"q{i}"] for i in range(5, 19)]

        try:
            # generate_profile 함수는 answer_indices를 이용해 프로필을 생성합니다.
            profile = generate_profile(answer_indices)
            return profile, 200
        except ValueError as ve:
            # 400-04: 응답이 존재하지 않습니다.
            abort(400, "400-04: 응답이 존재하지 않습니다")
        except Exception as e:
            # 500-00: 서버 내부 오류가 발생했습니다.
            abort(500, "500-00: 서버 내부 오류가 발생했습니다")
