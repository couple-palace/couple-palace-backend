# Dockerfile

FROM python:3.8-slim

MAINTAINER heumsi@gmail.com

RUN apt-get -y update && \
    apt-get install -y vim telnet wget

RUN python -m pip install --upgrade pip

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

#EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["app.py"]
