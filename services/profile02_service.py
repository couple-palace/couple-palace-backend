import openai
from flask import Flask

from config import load_secrets
from models.quiz_models import QuizQuestion, QuizOption
import requests
import os

load_secrets()

# 환경 변수에서 API_KEY 가져오기
API_KEY = os.getenv("API_KEY")

# 환경 변수에 없으면 GCP Cloud Metadata에서 가져오기
if not API_KEY:
    try:
        API_KEY = requests.get(
            "http://metadata.google.internal/computeMetadata/v1/project/attributes/API_KEY",
            headers={"Metadata-Flavor": "Google"}
        ).text.strip()
    except requests.exceptions.RequestException:
        API_KEY = None

# API_KEY가 없으면 오류 발생
if not API_KEY:
    raise ValueError("OPENAI API KEY가 설정되지 않았습니다! 환경 변수를 확인하세요.")

# OpenAI 클라이언트 초기화
client = openai.OpenAI(api_key=API_KEY)

# Flask 애플리케이션 초기화 (app.py에서 생성한 app 객체 사용)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')}"  # config.py에서 가져오기
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)  # app.py에서 초기화하므로 주석 처리


def get_question(question_id):
    from app import app
    with app.app_context():
        question = QuizQuestion.query.get(question_id)
        return question.question if question else "Unknown question"

def get_answer(question_id, answer_index):
    from app import app
    with app.app_context():
        question = QuizQuestion.query.get(question_id)
        if question:
            options = QuizOption.query.filter_by(question_id=question_id).all()
            if 0 <= answer_index < len(options):
                return options[answer_index].option_text
    return "Unknown answer"

def generate_profile(answer_indices,job):
    # MBTI
    # mbti_answers = answer_indices[:4]  # 1~4번 질문
    mbti_answers = [answer for i, answer in enumerate(answer_indices) if get_question_type(i + 1) == "MBTI"]  # MBTI 타입의 질문만 추출
    mbti = generate_mbti(mbti_answers)

    # NICK
    # nickname_answers = answer_indices[4:11]  # 5~11번 질문
    nickname_answers = [answer for i, answer in enumerate(answer_indices) if get_question_type(i + 1) == "NICK"]  # NICK 타입의 질문만 추출
    nickname_prompt = "\n".join([f"Q{i + 5}: {get_question(i + 5)}\nA: {get_answer(i + 5, answer)}" for i, answer in
                                 enumerate(nickname_answers)])
    nickname_prompt += "\n위의 답변을 바탕으로 닉네임을 생성해줘."
    nickname = generate_nickname(nickname_prompt, job)

    # COND
    # marriage_answers = answer_indices[11:]  # 12~18번 질문
    marriage_answers = [answer for i, answer in enumerate(answer_indices) if get_question_type(i + 1) == "COND"]  # COND 타입의 질문만 추출
    marriage_prompt = "\n".join([f"Q{i + 12}: {get_question(i + 12)}\nA: {get_answer(i + 12, answer)}" for i, answer in
                                 enumerate(marriage_answers)])
    marriage_prompt += "\n위의 답변을 바탕으로 결혼 조건 3가지를 생성해줘."
    marriage_conditions = generate_marriage_conditions(marriage_prompt)

    return {
        "mbti": mbti,
        "nickname": nickname,
        "marriage_conditions": marriage_conditions

    }

def get_question_type(question_number):
    # 질문 번호를 기준으로 QuizQuestion 테이블에서 해당 질문을 조회합니다.
    question = QuizQuestion.query.get(question_number)
    if question is None:
        # 질문 번호에 해당하는 질문이 없으면 None 혹은 적절한 기본값을 반환할 수 있습니다.
        return None
    return question.type

def generate_mbti(mbti_answers):
    # MBTI 매핑 테이블 (질문 ID 별 옵션 순서대로 MBTI 요소)
    mbti_mapping = {
        1: ["E", "I", "E", "I"],  # E/I 결정
        2: ["S", "N", "S", "N"],  # S/N 결정
        3: ["F", "F", "T", "T"],  # F/T 결정
        4: ["J", "P", "J", "P"]   # P/J 결정
    }

    # MBTI 코드 조합
    mbti_result = "".join(mbti_mapping[q_id][answer_idx] for q_id, answer_idx in enumerate(mbti_answers, start=1))
    return mbti_result

def generate_nickname(prompt, job):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "너는 연애 & 결혼에 관련된 닉네임을 지어주는 트위터 감성, 개웃긴 고딩이야"},
            {"role": "system", "content": "밈 감성, 트렌디한 형태의 형용사 또는 명사로 출력해줘"},
            {"role": "system", "content": "예를들어 '아내의 집밥 먹고 싶은', '지고지순 순정파','철학을 사랑한' 와 같이 50자 이내의 1개 닉네임을 지어줘"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=100
    )

    nickname1 = response.choices[0].message.content.strip()
    return f"{nickname1} {job}"


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
        max_tokens=500
    )
    return response.choices[0].message.content.strip().split('\n')
