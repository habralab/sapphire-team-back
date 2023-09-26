# Install requirements
FROM python:3.11-slim as core

WORKDIR /app

RUN pip install poetry==1.6.1
COPY ./poetry.lock /app/poetry.lock
COPY ./pyproject.toml /app/pyproject.toml
ENTRYPOINT ["poetry", "run"]

# Install deps for dev
FROM core as dev

RUN poetry install --with dev

# Install deps for app
FROM core as main

RUN poetry install --only main -E sqlite

# Lint
FROM dev as lint

COPY ./sapphire /app/sapphire
COPY ./autotests /app/autotests
COPY ./.pylintrc /app/.pylintrc
CMD ["pylint", "./sapphire", "./autotests"]

# Test
FROM dev as test

COPY ./sapphire /app/sapphire
COPY ./autotests /app/autotests
CMD ["pytest"]

# App
FROM main as app

COPY ./sapphire /app/sapphire
