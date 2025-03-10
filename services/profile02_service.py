import openai
from flask.cli import load_dotenv

from data.question import Nickname_Question_Answers, Marriage_Question_Answers
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.quiz_models import QuizQuestion, QuizOption


API_KEY = os.getenv("API_KEY")

if API_KEY is None:
    from dotenv import load_dotenv
    # load .env
    load_dotenv()
    API_KEY = os.environ.get('API_KEY')

# OpenAI 클라이언트 초기화
client = openai.OpenAI(api_key=API_KEY)

# Flask 애플리케이션 초기화 (app.py에서 생성한 app 객체 사용)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')}"  # config.py에서 가져오기
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)  # app.py에서 초기화하므로 주석 처리

def get_question(question_id):
    from app import app  # app 객체 임포트
    with app.app_context():  # Flask 애플리케이션 컨텍스트 내에서 쿼리 실행
        question = QuizQuestion.query.get(question_id)
        return question.question if question else "Unknown question"

def get_answer(question_id, answer_index):
    from app import app  # app 객체 임포트
    with app.app_context():  # Flask 애플리케이션 컨텍스트 내에서 쿼리 실행
        question = QuizQuestion.query.get(question_id)
        if question:
            options = QuizOption.query.filter_by(question_id=question_id).all()
            if 0 <= answer_index < len(options):
                return options[answer_index].option_text
    return "Unknown answer"

def generate_profile(answer_indices):
    nickname_answers = answer_indices[:7]  # 5~11번 질문 (7개)
    marriage_answers = answer_indices[7:]  # 12~18번 질문 (7개)

    nickname_prompt = "\n".join([f"Q{i + 5}: {get_question(i + 5)}\nA: {get_answer(i + 5, answer)}" for i, answer in enumerate(nickname_answers)])
    nickname_prompt += "\n위의 답변을 바탕으로 닉네임을 생성해줘."

    marriage_prompt = "\n".join([f"Q{i + 12}: {get_question(i + 12)}\nA: {get_answer(i + 12, answer)}" for i, answer in enumerate(marriage_answers)])
    marriage_prompt += "\n위의 답변을 바탕으로 결혼 조건 3가지를 생성해줘."

    nickname = generate_nickname(nickname_prompt)
    marriage_conditions = generate_marriage_conditions(marriage_prompt)

    return {
        "nickname": nickname,
        "marriage_conditions": marriage_conditions
    }

def generate_nickname(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "너는 연애& 결혼에 관련된 닉네임을 지어주는 트위터 감성, 개웃긴 고딩이야"},
            {"role": "system", "content": "'밈 감성 형용사 + 트렌디한 행동 패턴 + 직업 또는 특성'의 구조로 재미있는 닉네임을 지어줘"},
            {"role": "system", "content": "'아내의 집밥 먹고 싶은 인테리어 대표' 와 같이 50자 이내로 해줘"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

def generate_marriage_conditions(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "너는 연애와 결혼에 관련된 조건을 생성하는 분석적인 전문가야"},
            {"role": "system", "content": "트렌디하고 트위터에 돌아다닐만한 말투로, 개웃기게 해줘"},
            {"role": "system", "content": "주어진 답변을 바탕으로 3가지의 독특하고 재미있는 결혼 조건을 생성해줘"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].message.content.strip().split('\n')
