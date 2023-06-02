FROM python:3.11
LABEL authors="diego fonseca"

ARG APP_PATH=/var/app

WORKDIR ${APP_PATH}

COPY ./requirements.txt ${APP_PATH}/requirements.txt

RUN apt update && apt install -y --no-install-recommends && pip install --upgrade pip && pip install -r /var/app/requirements.txt

COPY . ${APP_PATH}
