# routes/common_routes.py

from flask import Blueprint
from flask_restx import Api
from controllers.photo_controller import PhotoController
from controllers.profile02_controller import ProfileController


# Blueprint 생성
api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

api = Api(
    api_v1,
    version="1.0",
    title="API 문서",
    description="커플궁전 server API 명세서",
    doc="/swagger",
)

# 네임스페이스 생성
photo_ns = api.namespace("photo", description="배경제거 API")
profile_ns = api.namespace("profile", description="프로필 생성 API")

# 컨트롤러(Resource) 등록
# # 실제 경로는 /api/v1/remove/bg
photo_ns.add_resource(PhotoController, "/remove/bg", endpoint="remove_bg")
# 실제 경로는 /api/v1/remove/bg
profile_ns.add_resource(ProfileController, "/generate/pf", endpoint="generate_profile")