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

# 요청 본문의 JSON 구조 모델 정의
# 각 질문은 question_idx, answer_idx, type으로 구성된 객체로 나타내며,
# 전체 요청은 questionsList (질문 객체들의 리스트)와 job (직업 정보)를 포함
question_model = profile_ns.model('Question', {
    'question_idx': fields.Integer(required=True, description='질문 번호 (정수)'),
    'answer_idx': fields.Integer(required=True, description='응답 인덱스 (정수)'),
    'type': fields.String(required=True, description='질문 유형')
})
profile_model = profile_ns.model('ProfileRequest', {
    'questionsList': fields.List(fields.Nested(question_model), required=True, description='질문 리스트'),
    'job': fields.String(required=True, description='직업 정보')
})

# 컨트롤러와 연결 (Swagger에 JSON body로 표시됨)
@profile_ns.route("/generate/pf")
@profile_ns.expect(profile_model, validate=True)
class ProfileResource(ProfileController):
    pass