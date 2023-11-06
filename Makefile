lint:
	pylint ./autotests ./sapphire ./tests

test:
	pytest ./tests

autotests:
	pytest ./autotests

build:
	docker build -t sapphire --target slim .

down:
	docker stack rm sapphire

clean: down
	docker rmi sapphire --force

up: clean build
	sleep 15
	docker stack deploy -c docker-compose.yaml sapphire
