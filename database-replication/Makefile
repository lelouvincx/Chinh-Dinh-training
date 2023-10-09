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

# ============ Build images ============ 
build-upstream-app:
	docker build -t upstream-app:latest -f .docker/images/app/Dockerfile .

build-kafka-connect:
	docker build -t kafka-connect:latest -f .docker/images/kafka-connect/Dockerfile .

# ============ Testing, formatting, type checks, link checks ============ 
app-requirements:
	rm app/requirements.txt && \
		pip freeze > app/requirements.txt

db-docs:
	dbdocs build docs/wideworldimporters.dbml

diagram:
	rm docs/images/design_architecture.png && \
		python docs/diagram.py && \
		mv design_architecture.png docs/images/

format:
	python -m black -S --line-length 88 --preview ./app

lint:
	python -m ruff check --fix ./app/app

test:
	python -m pytest --log-cli-level info -p no:warnings -v ./app/tests/

cov:
	python -m pytest --log-cli-level info -p no:warnings --cov -v ./app/tests/

ci: db-docs diagram app-requirements format lint

# ============ Postgres + MSSQL ============ 
to-psql-default:
	@docker compose exec -it source_db psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/postgres

to-psql:
	@docker compose exec -it source_db psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

to-mssql:
	@docker compose exec -it sink_db bash -c '/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "${MSSQL_SA_PASSWORD}"'

# ============ Kafka ============ 
check-kafka:
	docker run -it --rm --network database-replication_kafka_networks bitnami/kafka:3.5 \
		kafka-topics.sh --list --bootstrap-server kafka-server:9092

check-kafka-connect:
	curl -s -X GET http://localhost:8083 | jq

show-connector-plugins:
	curl -s -X GET http://localhost:8083/connector-plugins | jq

show-connectors:
	curl -s -X GET http://localhost:8083/connectors | jq

show-source-db-connector:
	curl -s -X GET http://localhost:8083/connectors/source-db-connector\?expand\=status\&expand\=info | jq

list-topics-source-db-connector:
	curl -s -X GET http://localhost:8083/connectors/source-db-connector/topics | jq
