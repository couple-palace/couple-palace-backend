# routes/common_routes.py

from flask import Blueprint
from flask_restx import Api
from controllers.profile02_controller import ProfileController
from routes.photo_routes import photo_ns


# Blueprint 생성
api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

api = Api(
    api_v1,
    version="1.0",
    title="API 문서",
    description="커플궁전 server API 명세서",
    doc="/swagger",
)

##########################
## 배경 제거 API
##########################
api.add_namespace(photo_ns)

##########################
## 프로필 생성 API
##########################

# 네임스페이스 생성
profile_ns = api.namespace("profile", description="프로필 생성 API")

# 파일 업로드 파서 설정
profile_upload_parser = photo_ns.parser()
profile_upload_parser.add_argument(
    "responseList",
    location="files",
    type=dict,
    required=True,
    help="퀴즈 문항별 응답 값 (JSON)"
)

# Swagger에 파일 업로드 필드 추가
# 실제 경로는 /api/v1/remove/bg
@profile_ns.route("/generate/pf")
@profile_ns.expect(profile_upload_parser)
class ProfileResource(ProfileController):
    pass