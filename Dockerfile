# syntax=docker/dockerfile:1
FROM python:3.11-alpine
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY bot ./bot
COPY database ./bot
COPY admin.py run.py ./
COPY config.default.py config.py
