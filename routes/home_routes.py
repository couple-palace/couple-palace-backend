from flask import render_template, Blueprint

# 루트 경로는 api/version 연결 x
home_bp = Blueprint("home_bp", __name__)

@home_bp.route("/")
def index():
    return render_template("index.html", swagger_url="/api/v1/swagger", quiz_table_url="/quiz-table")

@home_bp.route("/quiz-table")
def quiz_table():
    return render_template("quiz_table.html")