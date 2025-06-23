# 💘 커플궁전 프로필 테스트 (Couple Palace Profile Test)

> 커플궁전은 유쾌하지만 진지하게,  
> 당신의 연애력과 결혼 조건을 분석합니다!
>
> https://www.couplegungjeon.store

**AI 기반 맞춤형 연애/결혼 성향 프로필 생성 웹 애플리케이션**

커플궁전은 사용자의 연애 및 결혼 가치관을 분석하고,  
개인화된 **닉네임**, **MBTI-like 성향 요약**, **결혼 조건**을 제공하는 프로필 테스트 서비스입니다.  
본 저장소는 해당 서비스를 위한 **Flask 기반 백엔드 API 서버**입니다.

---

## 📝 프로젝트 개요

### ✅ 주요 기능

- 사용자 이름 및 직업 정보 입력
- 연애·결혼 가치관에 대한 객관식 퀴즈 응답
- 프로필 이미지 업로드
- AI 기반 닉네임 및 결혼 조건 생성
- 응답 결과를 JSON 형태로 제공

---

## ⚙️ 기술 스택

> ✅ 기존 GCP 환경에서 AWS 기반으로 마이그레이션 완료

| 항목      | 기술                                         |
|-----------|----------------------------------------------|
| Language  | Python 3.11                                  |
| Framework | Flask, flask-restx                           |
| AI API    | OpenAI GPT    |
| Database  | SQLite (local), Amazon RDS (MySQL, prod)     |
| 배포      | AWS EC2 (Docker + Nginx + Gunicorn)          |
| 이미지 처리 | rembg, Pillow                              |
| 기타      | dotenv, SQLAlchemy

---

## 📁 디렉토리 구조

```
/flask-backend
├── /controllers    # API 로직 (Resource)
├── /models         # DB 모델 정의
├── /routes         # Blueprint 등록
├── /services       # 프롬프트 생성 / OpenAI 통신 로직
├── /static         # test images
├── /templates      # server default pages
├── app.py          # 앱 실행 진입점
├── config.py       # 환경변수
└── requirements.txt
```

---

## 🔍 APIs
| Method | Endpoint                      | 설명         | 담당자       |
|--------|-------------------------------|--------------|--------------|
| POST   | `/api/v1/photo/remove/bg`     | 이미지 배경 제거 | 이강희       |
| POST   | `/api/v1/profile/generate/pf` | 프로필 생성     | 이소민       |
| GET    | `/api/v1/quiz/quiz-list`      | 퀴즈 데이터 조회 | 이강희       |

### 📤 프로필 생성 응답 예시

```json
{
  "mbti": "ISFP",
  "nickname": "'신혼가전 엑셀러레이터'",
  "marriage_conditions": [
    "1. **주말 액티비티 필수 조항**: 결혼 후 주말에는 아침부터 옷을 차려입고 나가야 한다! 집에 있으면 답답하니까, 외부에서 웃음이 터지게 하는 액티비티를 찾아야 해. (예: 놀이공원, 코미디 클럽, 아니면 그냥 마트 가서 샴푸 고르기!)",
    "",
    "2. **신용카드 한도 비밀 조항**: 결혼하자마자 돈 관리는 내가 맡을게! 단, 너의 카드 한도는 비밀로 할 거야. 만약 한도 초과해서 쇼핑하면 “나는 연애 중” 이라는 알리바이를 세워줘야 해. (이건 진짜 어려운 비밀!)",
    "",
    "3. **웃음 보장 조항**: 배우자의 성격은 꼭 웃기는 사람이어야 해! 인생이 힘든데 결혼생활까지 빡세면 안 되니까, 매일매일 개그 한 스푼씩 추가해줘야 해. (결혼식에서 개그맨 초대하는 거 잊지 말기!)"
  ]
}
```

---

## ✅ 커밋 컨벤션

| 태그 | 설명 |
|------|------|
| `feat` | 기능 추가 |
| `fix` | 버그 수정 |
| `style` | 포맷/변수명 변경 |
| `chore` | 설정, 패키지 변경 |
| `docs` | 문서 수정 |

---

## 🌿 브랜치 전략

- `deploy`: 운영 배포용
- `develop/main`: 메인 개발 브랜치
- `develop/#[이슈번호]/기능명`: 기능 단위 브랜치

---

## 🚀 배포 정보

- **서버**: AWS EC2 (Docker + Gunicorn + Nginx)
- **도메인**: [https://server.couplegungjeon.store](https://server.couplegungjeon.store) (AWS Route53 관리)
- **HTTPS 인증서**: AWS Certificate Manager
- **트래픽 라우팅**: Application Load Balancer로 HTTPS 트래픽 처리

---

## 📍 외부 요청 흐름
```markdown
🧑‍💻 사용자 브라우저 (https://www.couplegungjeon.store)
        │
        ▼
📨 API 요청 (예: axios 등)
        │
        ▼
🔗 API 주소: https://server.couplegungjeon.store
        │
        ▼
🌐 Nginx (AWS EC2)
    - 80 → 443 리다이렉트
    - 443 → 내부 포트 5000번 포워딩
        │
        ▼
🐳 Docker 컨테이너 내부 Flask + Gunicorn (5000번 포트)
```
---

## 📊 메트릭 시각화 (Prometheus + Grafana)

- 내부에서 시각화 서비스 제공
- Prometheus Exporter는 `9090` 포트로 서비스 중
- Grafana는 EC2 내부 IP로 접속 가능 (현재는 IP 기반 접근만 허용)

```
[관리자만 접근 가능]

http://<EC2-INSTANCE-IP>:9090   → Prometheus UI
http://<EC2-INSTANCE-IP>:3000   → Grafana (구성된 경우)
```

---

## 🧪 실행 가이드 (Local)

```bash
git clone https://github.com/couple-palace/couple-palace-backend.git
cd couple-palace-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
