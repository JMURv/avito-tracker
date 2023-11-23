FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ./app/bot

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY ./bot/poetry.lock ./bot/pyproject.toml ./

RUN pip install poetry
RUN poetry config installer.max-workers 10
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY ./bot ./
RUN chmod +x ./scripts/install_db.py
RUN chmod +x ./run.py
