
import openai
from config import OPENAI_API_KEY
from data.questions_and_answers import QUESTIONS_AND_ANSWERS

openai.api_key = OPENAI_API_KEY

def generate_profile(answer_indices):
    user_answers = []
    for i, answer_index in enumerate(answer_indices):
        if answer_index < 1 or answer_index > 4:
            raise ValueError(f"Invalid answer index for question {i+1}")
        user_answers.append(QUESTIONS_AND_ANSWERS[i]["answers"][answer_index - 1])

    nickname_prompt = "\n".join([f"Q{i+1}: {QUESTIONS_AND_ANSWERS[i]['question']}\nA{i+1}: {user_answers[i]}" for i in range(7)])
    nickname_prompt += "\n위의 답변을 바탕으로 닉네임을 생성해주세요."

    marriage_prompt = "\n".join([f"Q{i+1}: {QUESTIONS_AND_ANSWERS[i]['question']}\nA{i+1}: {user_answers[i]}" for i in range(7)])
    marriage_prompt += "\n위의 답변을 바탕으로 결혼 조건 4가지를 생성해주세요."

    nickname = generate_nickname(nickname_prompt)
    marriage_conditions = generate_marriage_conditions(marriage_prompt)

    return {
        "nickname": nickname,
        "marriage_conditions": marriage_conditions
    }

def generate_nickname(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 연애& 결혼에 관련된 닉네임을 지어주는 트위터 감성, 개웃긴 고딩이야"},
            {"role": "system", "content": "'밈 감성 형용사 + 트렌디한 행동 패턴 + 직업 또는 특성'의 구조로 재미있는 닉네임을 지어줘"},
            {"role": "system", "content": "'아내의 집밥 먹고 싶은 인테리어 대표' 와 같이 50자 이내로 해줘"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=100
    )
    return response.choices[0].message['content'].strip()

def generate_marriage_conditions(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 연애와 결혼에 관련된 조건을 생성하는 전문가야"},
            {"role": "system", "content": "주어진 답변을 바탕으로 4가지의 독특하고 재미있는 결혼 조건을 생성해줘"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].message['content'].strip().split('\n')