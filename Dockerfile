FROM python:3.14-slim-trixie

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ="UTC"
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt -y install -qq curl libffi-dev && \
    apt -y clean

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . /app
COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

WORKDIR /app
