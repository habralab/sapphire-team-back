OSFLAG :=
ifeq ($(OS),Windows_NT)
    OSFLAG = WIN
else
    OSFLAG = UNIX
endif

isort:
	isort --check .

lint:
	pylint autotests collabry tests

test:
	pytest tests

autotests:
	pytest autotests

build:
	docker build -t collabry --target slim .

down:
	docker stack rm collabry || true

clean:
	docker rmi collabry --force

sleep:
ifeq ($(OSFLAG),WIN)
	timeout /t 15
else
	sleep 15
endif

restart:
	docker stack deploy -c docker-compose.yaml collabry

up: clean build down sleep restart
