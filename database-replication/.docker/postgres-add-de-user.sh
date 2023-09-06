#!/bin/bash
set -e

PGPASSWORD=${POSTGRES_PASSWORD} psql -v ON_ERROR_STOP=1 --username ${POSTGRES_USER} --dbname ${POSTGRES_DB} <<-EOSQL
	  CREATE USER data_engineer;
	  GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO data_engineer;
EOSQL
