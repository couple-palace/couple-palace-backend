from flask_restx import Namespace
from werkzeug.datastructures import FileStorage
from controllers.photo_controller import PhotoController

# 네임스페이스 등록
photo_ns = Namespace("photo", description="배경제거 API")

# 파일 업로드 파서 설정 (여기에서 한 번만 정의)
photo_upload_parser = photo_ns.parser()
photo_upload_parser.add_argument(
    "content_image",
    location="files",
    type=FileStorage,
    required=True,
    help="배경을 제거할 이미지 파일 (JPEG, PNG 지원)"
)

# 컨트롤러와 연결 (Swagger에서 photo_upload_parser 사용)
@photo_ns.route("/remove/bg")
@photo_ns.expect(photo_upload_parser)  # ✅ 중복 선언 없이 사용
class PhotoRemoveResource(PhotoController):
    pass