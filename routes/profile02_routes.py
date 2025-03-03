# routes/profile_routes.py

from flask import Blueprint
from flask_restx import Api, Namespace
from controllers.profile02_controller import ProfileController

# 프로필 API를 위한 새로운 네임스페이스 생성
profile_ns = Namespace("profile", description="프로필 생성 API")

# 프로필 컨트롤러(Resource) 등록: 실제 경로는 /api/v1/remove/bg
profile_ns.add_resource(ProfileController, "/generate/pf", endpoint="generate_profile")
