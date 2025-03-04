from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.quiz_models import QuizQuestion, QuizOption