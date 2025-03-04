# SERVER_NAME = "server.couplegungjeon.store"

"""DB 설정 - DEV"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # ✅ SQLite 데이터베이스 파일 경로 명확하게 지정
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

