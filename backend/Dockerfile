FROM python:3.11.3-alpine3.18

WORKDIR /usr/src/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add gcc
RUN apk add gcc python3-dev
RUN apk add gcc postgresql-dev
RUN apk add gcc musl-dev

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .
