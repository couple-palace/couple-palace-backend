# routes/test_routes.py

from flask import Blueprint
from flask_restx import Api
from controllers.photo_controller import PhotoController
from routes.profile02_routes import profile_ns


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
ns = api.namespace("photo", description="배경제거 API")

# 컨트롤러(Resource) 등록: 실제 경로는 /api/v1/remove/bg
ns.add_resource(PhotoController, "/remove/bg", endpoint="remove_bg")

#profile_ns를 추가
api.add_namespace(profile_ns)