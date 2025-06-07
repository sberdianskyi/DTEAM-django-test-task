FROM python:3.12.10-bookworm
LABEL maintainer="sberdianskyi@gmail.com"
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN useradd -ms /bin/bash appuser
USER appuser
