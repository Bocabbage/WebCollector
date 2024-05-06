FROM python:3.10

COPY ./mikanani-v2/configs /app
WORKDIR /app

RUN ["pip", "install", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "-r", "requirements.txt"]