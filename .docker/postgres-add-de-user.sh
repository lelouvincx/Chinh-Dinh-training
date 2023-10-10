#!/bin/bash
set -e

PGPASSWORD=${POSTGRES_PASSWORD} psql -v ON_ERROR_STOP=1 --username ${POSTGRES_USER} --dbname ${POSTGRES_DB} <<-EOSQL
	  CREATE USER azure_pg_admin;
	  GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO azure_pg_admin;

	  CREATE USER azure_superuser;
	  ALTER USER azure_superuser WITH SUPERUSER;
	  GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO azure_superuser;

	  CREATE USER greglow;
	  GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO greglow;

	  CREATE USER data_engineer WITH PASSWORD '${POSTGRES_DE_PASSWORD}';
	  ALTER USER data_engineer WITH REPLICATION;
	  GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO data_engineer;
EOSQL