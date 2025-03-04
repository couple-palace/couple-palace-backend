from flask_restx import Resource, reqparse, abort
from flask import send_file
from werkzeug.datastructures import FileStorage
import os
from services.photo_service import process_image

upload_parser = reqparse.RequestParser()
upload_parser.add_argument(
    "content_image",
    location="files",
    type=FileStorage,
    required=True,
    help="배경을 제거할 이미지 파일 (JPEG, PNG 지원)"
)

class PhotoController(Resource):
    def post(self):
        args = upload_parser.parse_args()
        content_file = args.get("content_image")

        # 빈 파일명 검사
        if not content_file or content_file.filename == "":
            abort(400, "400-01: 파일이 비어 있습니다")  # 400-01: 파일이 비어 있습니다

        # 이미지 처리 (배경 제거) 수행
        try:
            output_path = process_image(content_file)
        except ValueError:
            abort(400, "400-02: 배경 제거에 실패했습니다")  # 400-02: 배경 제거에 실패했습니다
        except Exception:
            abort(500, "500-00: 서버 내부 오류가 발생했습니다")  # 500-00: 서버 내부 오류가 발생했습니다

        # 결과 이미지 반환 (JSON 응답 X, 이미지 파일 전송)
        try:
            return send_file(output_path, mimetype="image/png")  # 200: (이미지 전송)
        finally:
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except PermissionError:
                    pass