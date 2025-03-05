# routes/common_routes.py

from flask import Blueprint
from flask_restx import Api
from routes.photo_routes import photo_ns
from routes.profile_routes import profile_ns
from flask_sqlalchemy import SQLAlchemy

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
api.add_namespace(profile_ns)