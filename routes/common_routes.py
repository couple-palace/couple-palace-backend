# routes/common_routes.py

from flask import Blueprint
from flask_restx import Api
from werkzeug.datastructures import FileStorage
from controllers.photo_controller import PhotoController
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
api.add_namespace(photo_ns)

##########################
## 배경 제거 API
##########################

# # 네임스페이스 생성
# photo_ns = api.namespace("photo", description="배경제거 API")
#
# # 파일 업로드 파서 설정
# photo_upload_parser = photo_ns.parser()
# photo_upload_parser.add_argument(
#     "content_image",
#     location="files",
#     type=FileStorage,
#     required=True,
#     help="배경을 제거할 이미지 파일 (JPEG, PNG 지원)"
# )
#
# # Swagger에 파일 업로드 필드 추가
# # 실제 경로는 /api/v1/remove/bg
# @photo_ns.route("/remove/bg")
# @photo_ns.expect(photo_upload_parser)
# class PhotoRemoveResource(PhotoController):
#     pass

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