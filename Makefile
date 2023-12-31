OSFLAG :=
ifeq ($(OS),Windows_NT)
    OSFLAG = WIN
else
    OSFLAG = UNIX
endif

isort:
	isort --check .

lint:
	pylint ./autotests ./sapphire ./tests

test:
	pytest ./tests

autotests:
	pytest ./autotests

build:
	docker build -t sapphire --target slim .

down:
	docker stack rm sapphire || true

clean: down
	docker rmi sapphire --force

up: clean build
ifeq ($(OSFLAG),WIN)
	timeout /t 15
else
	sleep 15
endif
	docker stack deploy -c docker-compose.yaml sapphire
