from PIL import Image
from rembg import remove
import tempfile
import gc
import pillow_heif

# HEIF/HEIC 이미지 처리를 Pillow에서 가능하게 등록
pillow_heif.register_heif_opener()

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'heif', 'heic'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def process_image(content_file):
    if content_file.content_length > MAX_FILE_SIZE:
        raise Exception("파일 크기가 너무 큽니다. 최대 5MB 이하의 파일만 업로드 가능합니다.")

    filename = content_file.filename
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

    # 파일 확장자가 이미지 형식인지 체크
    if not allowed_file(filename):
        raise Exception("업로드된 파일이 이미지 형식이 아닙니다.")

    try:
        # 이미지 열기 (HEIC 포함 자동 인식됨)
        image = Image.open(content_file)

        # GIF 처리 (첫 프레임만 사용)
        if ext == 'gif':
            image.seek(0)

        image = image.convert("RGBA")

        # 배경 제거
        result = remove(image)

        # 임시 파일에 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            output_path = temp_file.name
            result.save(output_path, format="PNG")

        return output_path

    except Exception as e:
        raise Exception(f"이미지 처리 중 오류가 발생했습니다: {str(e)}")

    finally:
        # 메모리 해제
        if 'image' in locals():
            del image
        if 'result' in locals():
            del result
        gc.collect()