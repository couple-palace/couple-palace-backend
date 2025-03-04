# controllers/photo_controller.py

from flask_restx import Resource, reqparse, abort
from flask import send_file
from werkzeug.datastructures import FileStorage
from services.photo_service import process_image
import os

# 업로드 파서 생성: 'content_image' 파일 필드 (필수)
upload_parser = reqparse.RequestParser()
upload_parser.add_argument(
    "content_image", location="files", type=FileStorage, required=True
)


class PhotoController(Resource):
    def post(cls):
        args = upload_parser.parse_args()
        content_file = args.get("content_image")

        # 빈 파일명 검사
        if content_file.filename == "":
            abort(400, "Empty filename")

        # 이미지 처리 (배경 제거) 수행
        try:
            output_path = process_image(content_file)
        except ValueError as ve:
            abort(400, str(ve))
        except Exception as e:
            abort(500, str(e))

        # 결과 파일을 읽어 클라이언트에 전송
        try:
            with open(output_path, "rb") as f:
                return send_file(f, mimetype="image/png")
        finally:
            # 임시 파일 삭제 (파일 삭제 실패 시 무시)
            if "output_path" in locals():
                try:
                    os.remove(output_path)
                except PermissionError:
                    pass
