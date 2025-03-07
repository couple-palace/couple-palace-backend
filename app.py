# app.py

import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from routes.home_routes import home_bp
from routes.common_routes import api_v1
from config import Config
from models import db
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)
db.init_app(app)
app.register_blueprint(home_bp)
app.register_blueprint(api_v1)

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("🔍 TEMPLATE FOLDER PATH:", os.path.join(os.getcwd(), "templates"))
    print("🔍 TEMPLATES EXISTS?:", os.path.exists(os.path.join(os.getcwd(), "templates/index.html")))
    with app.app_context():
        print("🔧 Creating tables in SQLite database...")
        db.create_all()
        print("✅ Tables created successfully!")
    app.run(host="0.0.0.0", port=port, debug=True)
