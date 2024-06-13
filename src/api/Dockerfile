FROM python:3.11-slim-bookworm

USER daemon

WORKDIR /app

COPY requirements.txt .
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
