import openai
from flask import Flask
from config import load_secrets
from models.quiz_models import QuizQuestion, QuizOption
import os

# 비밀 설정 로드
load_secrets()

# 환경 변수에서 API 키 가져오기
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("OPENAI API KEY가 설정되지 않았습니다! 환경 변수를 확인하세요.")

# OpenAI 클라이언트 초기화
client = openai.OpenAI(api_key=API_KEY)

# Flask 앱 초기화
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 질문 조회
def get_question(question_id):
    from app import app
    with app.app_context():
        question = QuizQuestion.query.get(question_id)
        return question.question if question else "Unknown question"

# 보기 조회
def get_answer(question_id, answer_index):
    from app import app
    with app.app_context():
        question = QuizQuestion.query.get(question_id)
        if question:
            options = QuizOption.query.filter_by(question_id=question_id).all()
            if 0 <= answer_index < len(options):
                return options[answer_index].option_text
    return "Unknown answer"

# 질문 타입 조회
def get_question_type(question_id):
    question = QuizQuestion.query.get(question_id)
    return question.type if question else None

# 전체 프로필 생성
def generate_profile(answer_list, job):
    mbti_answers = []
    nickname_prompts = []
    marriage_prompts = []

    for item in answer_list:
        qid = item["question_idx"]
        aidx = item["answer_idx"]
        qtype = item["type"]

        question_text = get_question(qid)
        answer_text = get_answer(qid, aidx)

        if qtype == "MBTI":
            mbti_answers.append((qid, aidx))
        elif qtype == "NICK":
            nickname_prompts.append(f"Q{qid}: {question_text}\nA: {answer_text}")
        elif qtype == "COND":
            marriage_prompts.append(f"Q{qid}: {question_text}\nA: {answer_text}")

    mbti = generate_mbti(mbti_answers)

    nickname_prompt = "\n".join(nickname_prompts) + "\n위의 답변을 바탕으로 닉네임을 생성해줘."
    nickname = generate_nickname(nickname_prompt, job)

    marriage_prompt = "\n".join(marriage_prompts) + "\n위의 답변을 바탕으로 결혼 조건 3가지를 생성해줘."
    marriage_conditions = generate_marriage_conditions(marriage_prompt)

    return {
        "mbti": mbti,
        "nickname": nickname,
        "marriage_conditions": marriage_conditions
    }

# MBTI 생성
def generate_mbti(mbti_answers):
    mbti_mapping = {
        1: ["E", "I", "E", "I"],
        2: ["S", "N", "S", "N"],
        3: ["F", "F", "T", "T"],
        4: ["J", "P", "J", "P"]
    }
    mbti_result = "".join(
        mbti_mapping[qid][aidx] for qid, aidx in mbti_answers if qid in mbti_mapping
    )
    return mbti_result

# 닉네임 생성
def generate_nickname(prompt, job):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "너는 연애 & 결혼에 관련된 닉네임을 지어주는 트위터 감성, 개웃긴 고딩이야"},
            {"role": "system", "content": "틱톡, 트위터, 인터넷 밈 감성, 트렌디한 형태의 형용사 또는 명사로 출력해주되, 주술관계, 목적어와의 호응이 자연스러워야 해"},
            {"role": "system", "content": "예를들어 '아내의 집밥 먹고 싶은', '지고지순 순정파','철학을 사랑한' 와 같이 50자 이내의 1개 닉네임을 지어줘"},
            {"role": "user", "content": f"{prompt}\n참고로 사용자의 직업은 '{job}'인데, 이걸 한국어로 자연스럽게 바꿔서 닉네임에 녹여줘."}
        ],
        temperature=0.7,
        max_tokens=100
    )
    nickname1 = response.choices[0].message.content.strip()
    # return f"{nickname1} {job}"
    return nickname1

# 결혼 조건 생성
def generate_marriage_conditions(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "너는 연애와 결혼에 관련된 조건을 생성하는 분석적인 전문가야"},
            {"role": "system", "content": "응답 형식은:\n1. 조건 제목\n조건 설명 (다음 줄에)\n2. 조건 제목\n조건 설명 (다음 줄에)\n이런 식으로 줄바꿈을 반드시 해줘!"},
            {"role": "system", "content": "트렌디하고 트위터에 돌아다닐만한 말투로, 개웃기게 해줘"},
            {"role": "system", "content": "주어진 답변을 바탕으로 3가지의 독특하고 재미있는 결혼 조건을 생성해줘"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content.strip().split('\n')