from flask_restx import Namespace, reqparse
from controllers.profile02_controller import ProfileController

# 네임스페이스 등록
profile_ns = Namespace("profile", description="프로필 생성 API")

# JSON 요청 파서 설정
profile_upload_parser = profile_ns.parser()
for i in range(7):
    profile_upload_parser.add_argument(
        f"q{i+1}",
        type=int,
        required=True,
        help=f"질문 {i+1} 번에 대한 응답은 공백이 불가합니다"
    )

# 컨트롤러와 연결 (Swagger에서 profile_upload_parser 사용)
@profile_ns.route("/generate/pf")
@profile_ns.expect(profile_upload_parser)
class ProfileResource(ProfileController):
    pass
