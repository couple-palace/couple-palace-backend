from flask_restx import Api, Resource, reqparse
from flask import Flask, request, send_file
from werkzeug.datastructures import FileStorage
from PIL import Image
from rembg import remove
import tempfile
import os

app = Flask(__name__)
api = Api(app, version='1.0', title='API 문서', description='Swagger 문서', doc="/api-couple")

test_api = api.namespace('test', description='배경제거 API')

upload_parser = api.parser()
upload_parser.add_argument('content_image', location='files', type=FileStorage, required=True)


@test_api.route('/api/v1/remove/bg')
@api.expect(upload_parser)
class Test(Resource):
    @api.doc('배경 제거')
    def post(self):
        args = upload_parser.parse_args()
        content_file = args['content_image']

        if content_file.filename == '':
            api.abort(400, "Empty filename")

        try:
            content_image = Image.open(content_file).convert('RGBA')
        except Exception as e:
            api.abort(400, f"Invalid image format: {str(e)}")

        try:
            output_image = remove(content_image)

            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                output_path = temp_file.name
                output_image.save(output_path, format='PNG')

            with open(output_path, 'rb') as f:
                return send_file(f, mimetype='image/png')

        except Exception as e:
            api.abort(500, f"Error processing image: {str(e)}")
        finally:
            if 'output_path' in locals():
                try:
                    os.remove(output_path)
                except PermissionError:
                    pass  # 파일을 삭제할 수 없는 경우 무시


if __name__ == '__main__':
    app.run(debug=True)
