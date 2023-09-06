include .env

# Docker compose
build:
	docker compose build

up:
	docker compose up

up-d:
	docker compose up -d

up-build:
	docker compose up --build

down:
	docker compose down

restart:
	docker compose down && docker compose up

restart-d:
	docker compose down && docker compose up -d

# Postgres
to-psql:
	docker compose exec -it source_db psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

.SILENT:
	to-psql
