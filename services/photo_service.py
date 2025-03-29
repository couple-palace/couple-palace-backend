from PIL import Image
from rembg import remove
import tempfile
import pyheif

def process_image(content_file):
    """
    업로드된 이미지 파일을 열어서 RGBA로 변환한 후, 배경 제거 처리를 진행합니다.
    iOS 기기에서 업로드된 HEIC/HEIF 파일일 경우 Pillow가 직접 열지 못하므로,
    pyheif를 사용해 변환 후 처리합니다.
    """
    filename = content_file.filename
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

    # HEIC/HEIF 파일이면 pyheif로 읽어서 Pillow 이미지 객체로 변환
    if ext in ['heic', 'heif']:
        try:
            heif_file = pyheif.read(content_file)
            content_image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride
            ).convert("RGBA")
        except Exception as e:
            raise ValueError(f"HEIC 이미지 변환에 실패했습니다: {str(e)}")
    else:
        try:
            content_image = Image.open(content_file).convert("RGBA")
        except Exception as e:
            raise ValueError(f"이미지 형식이 올바르지 않습니다: {str(e)}")

    # 배경 제거 처리 후 PNG로 저장
    try:
        output_image = remove(content_image)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            output_path = temp_file.name
            output_image.save(output_path, format="PNG")
        return output_path
    except Exception as e:
        raise Exception(f"이미지 처리 중 오류가 발생했습니다: {str(e)}")