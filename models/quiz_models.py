from models import db

# 질문 정보 저장
class QuizQuestion(db.Model):
    __tablename__ = "quiz_questions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(50), nullable=False)  # MBTI, NICK, COND
    question = db.Column(db.Text, nullable=False)

# 각 질문에 대한 선택지 저장 (외래키)
class QuizOption(db.Model):
    __tablename__ = "quiz_options"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey("quiz_questions.id"), nullable=False)
    option_text = db.Column(db.Text, nullable=False)

    question = db.relationship("QuizQuestion", backref=db.backref("options", lazy=True))