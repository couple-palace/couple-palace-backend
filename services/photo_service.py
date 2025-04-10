from PIL import Image
from rembg import remove
import tempfile
import gc
import pillow_heif

# HEIF/HEIC 이미지 처리를 Pillow에서 가능하게 등록
pillow_heif.register_heif_opener()

MAX_WIDTH = 1024
MAX_HEIGHT = 1024

def process_image(content_file):
    filename = content_file.filename
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

    try:
        # 이미지 열기 (HEIC 포함 자동 인식됨)
        image = Image.open(content_file)

        # GIF 처리 (첫 프레임만 사용)
        if ext == 'gif':
            image.seek(0)

        image = image.convert("RGBA")

        # 이미지 크기 제한
        if image.width > MAX_WIDTH or image.height > MAX_HEIGHT:
            image.thumbnail((MAX_WIDTH, MAX_HEIGHT))

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