# SERVER_NAME = "server.couplegungjeon.store"

import os
from google.cloud import secretmanager

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Secret을 실행 전에 미리 불러와 환경변수로 설정
def load_secrets():
    client = secretmanager.SecretManagerServiceClient()
    project_id = "alpine-anvil-452303-u8"

    secret_keys = ["FLASK_SECRET_KEY", "DB_URI", "API_KEY"]

    for secret_id in secret_keys:
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        os.environ[secret_id] = response.payload.data.decode("UTF-8")


# 앱 시작 전에 Secret을 미리 가져와 환경변수에 저장
load_secrets()


class Config:
    # # SQLite connection
    # SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
