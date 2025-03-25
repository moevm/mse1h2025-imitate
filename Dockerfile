FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . /app/

WORKDIR /app/mse1h2025_imitate

RUN pip install --upgrade pip && pip install --extra-index-url https://download.pytorch.org/whl/cpu -r /app/requirements.txt

EXPOSE 8000
