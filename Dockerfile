# Install requirements
FROM python:3.11-slim as core

WORKDIR /app

RUN pip install poetry==1.6.1
COPY ./poetry.lock /app/poetry.lock
COPY ./pyproject.toml /app/pyproject.toml

# Testing
FROM core as test

RUN poetry install --with dev -E sqlite
COPY ./.pylintrc /app/.pylintrc
COPY ./sapphire /app/sapphire
COPY ./autotests /app/autotests
COPY ./tests /app/tests
ENTRYPOINT ["poetry", "run"]

# Application
FROM core as app

RUN poetry install --only main -E sqlite
COPY ./sapphire /app/sapphire
ENTRYPOINT ["poetry", "run", "python", "-m", "sapphire"]
