from flask_restx import Namespace, fields
from controllers.profile02_controller import ProfileController

# 네임스페이스 등록
profile_ns = Namespace("profile", description="프로필 생성 API")

# # JSON 요청 파서 설정
# profile_upload_parser = profile_ns.parser()
# for i in range(1, 19):
#     profile_upload_parser.add_argument(
#         f"q{i}",
#         type=int,
#         required=True,
#         help=f"질문 {i} 번에 대한 응답은 공백이 불가합니다",
#         location="json"
#     )

# 요청 본문의 JSON 구조 모델 정의 (q1 ~ q18)
profile_model = profile_ns.model('ProfileRequest', {
    'q1': fields.Integer(required=True, description='질문 1 응답 (정수)'),
    'q2': fields.Integer(required=True, description='질문 2 응답 (정수)'),
    'q3': fields.Integer(required=True, description='질문 3 응답 (정수)'),
    'q4': fields.Integer(required=True, description='질문 4 응답 (정수)'),
    'q5': fields.Integer(required=True, description='질문 5 응답 (정수)'),
    'q6': fields.Integer(required=True, description='질문 6 응답 (정수)'),
    'q7': fields.Integer(required=True, description='질문 7 응답 (정수)'),
    'q8': fields.Integer(required=True, description='질문 8 응답 (정수)'),
    'q9': fields.Integer(required=True, description='질문 9 응답 (정수)'),
    'q10': fields.Integer(required=True, description='질문 10 응답 (정수)'),
    'q11': fields.Integer(required=True, description='질문 11 응답 (정수)'),
    'q12': fields.Integer(required=True, description='질문 12 응답 (정수)'),
    'q13': fields.Integer(required=True, description='질문 13 응답 (정수)'),
    'q14': fields.Integer(required=True, description='질문 14 응답 (정수)'),
    'q15': fields.Integer(required=True, description='질문 15 응답 (정수)'),
    'q16': fields.Integer(required=True, description='질문 16 응답 (정수)'),
    'q17': fields.Integer(required=True, description='질문 17 응답 (정수)'),
    'q18': fields.Integer(required=True, description='질문 18 응답 (정수)')
})

# 컨트롤러와 연결 (Swagger에 JSON body로 표시됨)
@profile_ns.route("/generate/pf")
@profile_ns.expect(profile_model, validate=True)
class ProfileResource(ProfileController):
    pass