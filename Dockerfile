# Install requirements
FROM python:3.11-slim as core

WORKDIR /app

RUN pip install poetry==1.6.1
COPY ./poetry.lock /app/poetry.lock
COPY ./pyproject.toml /app/pyproject.toml

# All requirements
FROM core as full

RUN poetry install --with dev --all-extras
COPY ./.pylintrc /app/.pylintrc
COPY ./sapphire /app/sapphire
COPY ./autotests /app/autotests
COPY ./tests /app/tests
ENTRYPOINT ["poetry", "run"]

# Only application
FROM core as slim

RUN apt update -y && apt install -y curl

RUN poetry install --only main --all-extras
COPY ./sapphire /app/sapphire
ENTRYPOINT ["poetry", "run", "python", "-m", "sapphire"]
