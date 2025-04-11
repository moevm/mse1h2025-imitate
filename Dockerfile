FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . /app/

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*S

RUN pip install --upgrade pip && \
    pip install --extra-index-url https://download.pytorch.org/whl/cpu -r /app/requirements.txt && \
    pip cache purge

EXPOSE 8000