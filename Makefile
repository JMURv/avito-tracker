prod:
	docker-compose up

down:
	docker-compose down

rebuild:
	docker-compose down
	docker rmi avito_bot:latest
	docker-compose build --no-cache
