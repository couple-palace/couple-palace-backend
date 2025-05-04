SERVER_NAME = "server.couplegungjeon.store"
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Secret을 실행 전에 미리 불러와 환경변수로 설정
def load_secrets():
    secret_keys = ["FLASK_SECRET_KEY", "DB_URI", "API_KEY"]

    for key in secret_keys:
        value = os.getenv(key)
        if value:
            os.environ[key] = value
        else:
            raise EnvironmentError(f"Missing required secret: {key}")


# 앱 시작 전에 Secret을 미리 가져와 환경변수에 저장
load_secrets()


class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
