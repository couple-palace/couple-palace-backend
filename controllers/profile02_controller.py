from flask import request
from flask_restx import Resource, abort
from services.profile02_service import generate_profile


class ProfileController(Resource):
    def post(self):
        # 요청 본문에서 JSON 데이터를 파싱
        data = request.get_json(silent=True) # 요청 본문에 JSON 데이터가 없거나 유효하지 않을 경우 예외를 발생시키지 않고 대신 None을 반환하도록 하는 옵션
        if not data:
            abort(400, "400-04: JSON 본문이 필요합니다") # 400-04: JSON 본문이 필요합니다

        if data and "questionsList" in data and "job" in data:
            questions_list = data["questionsList"]
            job = data["job"]

            # questionsList가 리스트인지 확인
            if not isinstance(questions_list, list):
                abort(400, "400-08: questionsList는 리스트여야 합니다") # 400-08: questionsList는 리스트여야 합니다

            # 각 질문 항목은 dict여야 하며, question_idx, answer_idx, type을 포함
            answer_data = {}
            for q in questions_list:
                if not isinstance(q, dict):
                    abort(400, "400-05: 각 질문은 객체여야 합니다") # 400-05: 각 질문은 객체여야 합니다
                for attribute in ("question_idx", "answer_idx", "type"):
                    if attribute not in q:
                        abort(400, f"400-06: 각 질문은 '{attribute}'를 포함해야 합니다") # 400-06: 각 질문은 '{key}'를 포함해야 합니다
                    # question_idx와 answer_idx가 정수인지 검증
                try:
                    question_idx = int(q["question_idx"])
                    answer_idx = int(q["answer_idx"])
                except ValueError:
                    abort(400, "400-08: question_idx와 answer_idx는 정수여야 합니다") # 400-08: question_idx와 answer_idx는 정수여야 합니다

                # 검증 후 answer_data에 값 저장 (key는 "q{question_idx}" 형태)
                answer_data[f"q{question_idx}"] = answer_idx

            ####################################################################
            answer_indices = []
            for i in range(1, 19):
                key = f"q{i}"
                if key not in answer_data:
                    abort(400, f"400-09: 질문 {i} 번에 대한 응답이 누락되었습니다")  # 400-09: 질문 {i} 번에 대한 응답이 누락되었습니다
            # 서비스에는 기존과 같이 5번부터 18번까지의 응답 인덱스만 전달 (추후 수정 필요)
            answer_indices = [answer_data[f"q{i}"] for i in range(5, 19)]
            answer_indices.append(answer_data[key])
            ####################################################################

            try:
                ####################################################################
                # generate_profile 함수는 answer_indices를 이용해 프로필 생성 (추후 수정 필요)
                profile = generate_profile(answer_indices)
                # # generate_profile 함수는 answer_indices와 job을 사용해 프로필을 생성합니다.
                # profile = generate_profile(answer_indices, job)
                ####################################################################

                return profile, 200
            except ValueError as ve:
                abort(400, "400-07: 프로필을 생성할 수 없습니다") # 400-07: 프로필을 생성할 수 없습니다
            except Exception as e:
                abort(500, "500-00: 서버 내부 오류가 발생했습니다") # 500-00: 서버 내부 오류가 발생했습니다

        else:
            # JSON 방식이 아닐 경우 기존 reqparse 방식으로 처리 (URL 쿼리 파라미터 or form-data 방식)
            from flask_restx import reqparse

            profile_parser = reqparse.RequestParser()

            for i in range(1, 19):
                profile_parser.add_argument(
                    f"q{i}",
                    type=int,
                    required=True,
                    help=f"질문 {i} 번에 대한 응답은 공백이 불가합니다"
                )

            args = profile_parser.parse_args()

            # 서비스에는 기존과 같이 5번부터 18번까지의 응답 인덱스만 전달합니다.
            answer_indices = [args[f"q{i}"] for i in range(5, 19)]

            try:
                profile = generate_profile(answer_indices)
                return profile, 200
            except ValueError as ve:
                abort(400, "400-07: 프로필을 생성할 수 없습니다") # 400-07: 프로필을 생성할 수 없습니다
            except Exception as e:
                abort(500, "500-00: 서버 내부 오류가 발생했습니다")  # 500-00: 서버 내부 오류가 발생했습니다