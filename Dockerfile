# Install requirements
FROM python:3.11-slim as core

WORKDIR /app

RUN pip install poetry==1.6.1
COPY ./poetry.lock /app/poetry.lock
COPY ./pyproject.toml /app/pyproject.toml
ENTRYPOINT ["poetry", "run"]

# Install deps for dev
FROM core as dev

RUN poetry install --with dev -E sqlite

# Install deps for main
FROM core as main

RUN poetry install --only main -E sqlite

# Lint
FROM dev as lint

COPY ./sapphire /app/sapphire
COPY ./autotests /app/autotests
COPY ./tests /app/tests
COPY ./.pylintrc /app/.pylintrc
CMD ["pylint", "/app/sapphire", "/app/tests", "/app/autotests"]

# Isort
FROM dev as isort

COPY ./sapphire /app/sapphire
COPY ./tests /app/tests
COPY ./autotests /app/autotests
CMD ["isort", "--check", "/app/sapphire", "/app/tests", "/app/autotests"]

# Test
FROM dev as test

COPY ./sapphire /app/sapphire
COPY ./tests /app/tests
CMD ["pytest", "/app/tests"]

# Autotests
FROM dev as autotests

COPY ./sapphire /app/sapphire
COPY ./autotests /app/autotests
CMD ["pytest", "/app/autotests"]

# App
FROM main as app

COPY ./sapphire /app/sapphire
