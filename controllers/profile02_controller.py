from flask import request
from flask_restx import Resource, abort
from services.profile02_service import generate_profile


class ProfileController(Resource):
    def post(self):
        # 요청 본문에서 JSON 데이터를 파싱
        data = request.get_json()
        if not data:
            abort(400, "400-04: JSON 본문이 필요합니다") # 400-04: JSON 본문이 필요합니다

        # 요청 본문에서 q1 ~ q18 까지의 인자를 받도록 설정
        # 각 질문에 대한 응답은 필수, 정수형으로 전달
        answer_data = {}
        for i in range(1, 19):
            key = f"q{i}"
            if key not in data or data[key] is None:
                abort(400, f"400-05: 질문 {i} 번에 대한 응답은 공백이 불가합니다") # 400-05: 질문 {i} 번에 대한 응답은 공백이 불가합니다
            try:
                answer_data[key] = int(data[key])
            except ValueError:
                abort(400, f"400-06: 질문 {i} 번의 응답은 정수여야 합니다") # 400-06: 질문 {i} 번의 응답은 정수여야 합니다

        # 서비스에는 기존과 같이 5번부터 18번까지의 응답 인덱스만 전달
        answer_indices = [answer_data[f"q{i}"] for i in range(5, 19)]

        try:
            # generate_profile 함수는 answer_indices를 이용해 프로필 생성
            profile = generate_profile(answer_indices)
            return profile, 200
        except ValueError as ve:
            abort(400, "400-07: 프로필을 생성할 수 없습니다") # 400-07: 프로필을 생성할 수 없습니다
        except Exception as e:
            abort(500, "500-00: 서버 내부 오류가 발생했습니다") # 500-00: 서버 내부 오류가 발생했습니다
