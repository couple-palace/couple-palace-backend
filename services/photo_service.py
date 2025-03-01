# services/photo_service.py

from PIL import Image
from rembg import remove
import tempfile


def process_image(content_file):
    # 이미지 열기 및 RGBA 변환 (예외 발생 시 caller에서 처리)
    try:
        content_image = Image.open(content_file).convert("RGBA")
    except Exception as e:
        raise ValueError(f"Invalid image format: {str(e)}")

    # 배경 제거 처리 및 임시파일에 결과 저장
    try:
        output_image = remove(content_image)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            output_path = temp_file.name
            output_image.save(output_path, format="PNG")
        return output_path
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")
