include .env

# ============ Docker compose ============ 
build:
	docker compose build

up:
	docker compose up

up-d:
	docker compose up -d

up-build:
	docker compose up --build

up-build-d:
	docker compose up --build -d

down:
	docker compose down

restart: down up

restart-d: down up-d

restart-build-d: down up-build-d

sleep:
	sleep 20

# ============ Testing, formatting, type checks, link checks ============ 
app-requirements:
	rm app/requirements.txt && \
		pip freeze > app/requirements.txt

docs:
	dbdocs build docs/wideworldimporters.dbml

format:
	python -m black -S --line-length 88 --preview ./app

lint:
	python -m ruff check --fix ./app

test:
	python -m pytest --log-cli-level info -p no:warnings -v ./app

ci: docs app-requirements format lint

# ============ Postgres ============ 
to-psql-default:
	@docker compose exec -it source_db psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/postgres

to-psql:
	@docker compose exec -it source_db psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
