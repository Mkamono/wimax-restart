FROM python:latest

ENV PYTHONIOENCODING utf-8

#ライブラリインストール
COPY requirement.txt ./
RUN pip install -r requirement.txt

WORKDIR /src/app

CMD python3 main.py