# app.py

import os
from flask import Flask, render_template_string
from routes.common_routes import api_v1  # Blueprint 모듈 임포트
from config import Config
from models.quiz_models import db
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(api_v1)
db.init_app(app)

CORS(
    app,
    origins=[
        "https://www.couplegungjeon.store",
        "https://couplegungjeon.store",
        "https://35.216.111.96",
        "http://www.couplegungjeon.store",
        "http://couplegungjeon.store",
        "http://35.216.111.96",
        "http://localhost",
        "https://localhost",
    ],
)


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
    with app.app_context():
        print("🔧 Creating tables in SQLite database...")
        db.create_all()
        print("✅ Tables created successfully!")
    app.run(host="0.0.0.0", port=port, debug=True)
