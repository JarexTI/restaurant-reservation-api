.PHONY: up down build migrate logs start

up:
	docker-compose up -d --build

down:
	docker-compose down

build:
	docker-compose build

migrate:
	docker-compose exec backend alembic upgrade head

logs:
	docker-compose logs -f

start: up migrate logs

