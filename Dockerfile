# Python 3.8 Slim 이미지 사용
FROM python:3.8-slim

# 유지보수 정보
MAINTAINER heumsi@gmail.com

# 필수 패키지 설치
RUN apt-get update && \
    apt-get install -y vim telnet wget && \
    rm -rf /var/lib/apt/lists/*

# 최신 pip 설치
RUN python -m pip install --upgrade pip

# Gunicorn 설치 추가 ✅
RUN pip install gunicorn

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 복사 후 패키지 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 복사
COPY . /app

# 실행 포트 설정
EXPOSE 5000

# Gunicorn으로 실행하도록 변경 ✅
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app", "--forwarded-allow-ips=*"]