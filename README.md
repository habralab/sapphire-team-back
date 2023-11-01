# Sapphire Backend

![Stage Autotests Status](https://github.com/habralab/sapphire-team-back/actions/workflows/autotests-stage.yaml/badge.svg)

Backend for developer collaboration service

## Requirements

### Requirements: Docker

For running or testing all services you can use `Docker`. You can see instructions for installation
[here](https://docs.docker.com/engine/install/).

After installation you should init `swarm`
```shell
docker swarm init 
```

### Requirements: Python

For running or testing all services you can use `Python` environment. You can install Python on
your local machine directly (see [here](https://www.python.org/downloads/)) or use any wrappers
(`venv`, `pyenv`, `pipenv`, etc.).

**Python version: `3.11` or higher**

After installation Python you need install `poetry` (v1.6.1):
```shell
pip install poetry==1.6.1
```
And install all Python requirements:
```shell
poetry install --all-extras
```

## Test

### Test: Docker

For testing you should build full image

```shell
docker build -t sapphire --target full . 
```

**Lint**
```shell
docker run sapphire pylint /app/sapphire /app/autotests /app/tests
```

**Isort**
```shell
docker run sapphire isort .
```

**Unit tests**
```shell
docker run sapphire pytest /app/tests
```

**Autotests**
```shell
docker run sapphire pytest /app/autotests
```

### Test: Python

**Lint**
```shell
pylint /app/sapphire /app/autotests /app/tests
```

**Isort**
```shell
isort .
```

**Unit tests**
```shell
pytest /app/tests
```

**Autotests**
```shell
pytest /app/autotests
```

## Run

### Run: Docker

Copy `.env.example` to `.env`
```shell
cp .env.example .env
```

For running you should build app image
```shell
docker build -t sapphire --target slim .
```

Create secrets (you can get any values from `.env.example`)
```shell
echo "any_client_id" | docker secret create habr_oauth2_client_id -
echo "any_client_secret" | docker secret create habr_oauth2_client_secret -
echo "any_api_key" | docker secret create habr_api_key -
echo "any_password" | docker secret create postgresql_password -
echo "any_access_private_key" | docker secret create jwt_access_token_private_key -
echo "any_access_public_key" | docker secret create jwt_access_token_public_key -
echo "any_refresh_private_key" | docker secret create jwt_refresh_token_private_key -
echo "any_refresh_public_key" | docker secret create jwt_refresh_token_public_key -
```

Prepare storages
```shell
mkdir -p redis_data
mkdir -p database_data
mkdir -p broker_data/kafka/data
mkdir -p broker_data/zookeeper/data
mkdir -p broker_data/zookeeper/log
mkdir -p users_data/media
mkdir -p projects_data/media
```

And run
```shell
docker stack deploy -c docker-compose.yaml sapphire
```

Join to database service
```shell
docker exec -it -u postgres $(docker ps -q -f name=sapphire_database) psql
```

Create database for every service: `storage`, `users`, `projects`, `notifications` and `messenger`
```shell
CREATE ROLE service_name WITH LOGIN ENCRYPTED PASSWORD 'P@ssw0rd';
CREATE DATABASE service_name;
GRANT ALL PRIVILEGES ON DATABASE service_name TO service_name;
ALTER DATABASE service_name OWNER TO service_name;
```

### Run: Python

For running separate services, please, see documentation:
1. [Storage](sapphire/storage/README.md)
2. [Users](sapphire/users/README.md)
3. [Projects](sapphire/projects/README.md)
4. [Email](sapphire/email/README.md)
5. [Notifications](sapphire/notifications/README.md)
6. [Messenger](sapphire/messenger/README.md)
