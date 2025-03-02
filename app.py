# app.py

import os
from flask import Flask, render_template_string
from routes.photo_routes import api_v1  # Blueprint 모듈 임포트
import config


app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(api_v1)


@app.route("/")
def index():
    swagger_url = "/api/v1/swagger"  # 실제 Swagger UI URL
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome</title>
    </head>
    <body>
        <h1>Welcome to the API!</h1>
        <a href="{swagger_url}">
            <button>Swagger API Documentation</button>
        </a>
    </body>
    </html>
    """
    return render_template_string(html)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)