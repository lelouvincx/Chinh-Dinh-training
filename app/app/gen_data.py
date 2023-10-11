from sqlalchemy import text
from faker import Faker

try:
    # Try importing for unit testing
    from app.psql_connector import PsqlConnector
except ImportError:
    # Try importing for upstream app
    from psql_connector import PsqlConnector

import os
import logging
from os import environ as env
from dotenv import load_dotenv


# Init logger
logger = logging.getLogger(__name__)

# File handler
log_dir = os.path.dirname(__file__) + "/logs"
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

f_handler = logging.FileHandler(log_dir + f"/{__name__}.log")
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter("[ %(asctime)s - %(levelname)s - %(name)s ] %(message)s")
f_handler.setFormatter(f_format)

# Stream handler
s_handler = logging.StreamHandler()
s_handler.setLevel(logging.DEBUG)
s_format = logging.Formatter("[ %(asctime)s - %(levelname)s - %(name)s ] %(message)s")
s_handler.setFormatter(s_format)

# Add handlers
logger.addHandler(f_handler)
logger.addHandler(s_handler)


# Load environment variables
load_dotenv()
psql_params = {
    "host": env["POSTGRES_HOST"],
    "port": env["POSTGRES_PORT"],
    "user": env["POSTGRES_USER"],
    "password": env["POSTGRES_PASSWORD"],
    "database": env["POSTGRES_DB"],
}


fake = Faker()


class Table:
    def __init__(self, schema: str, name: str) -> None:
        self._schema = schema
        self._name = name
        self._attributes = []

    # Getters
    def get_schema(self) -> str:
        return self._schema

    def get_name(self) -> str:
        return self._name

    def get_attributes(self) -> list:
        return self._attributes

    # Setters
    def set_attributes(self, attributes: list) -> None:
        self._attributes = attributes

    # Methods
    def update_attributes(self, connector: PsqlConnector) -> bool:
        with connector.connect() as engine:
            with engine.connect() as cursor:
                sql_script = f"""
                    WITH rows AS (
	                    SELECT  c.relname AS table_name,
			                    a.attname AS attribute_name,
			                    a.attnotnull AS is_attribute_null,
			                    a.attnum AS attribute_num,
			                    t.typname AS type_name
	                    FROM    pg_catalog.pg_class c
		                JOIN    pg_catalog.pg_attribute a
		                    ON  c."oid" = a.attrelid AND a.attnum >= 0
		                JOIN    pg_catalog.pg_type t
		                    ON  t."oid" = a.atttypid
		                JOIN    pg_catalog.pg_namespace n
		                    ON  c.relnamespace = n."oid"
	                    WHERE   n.nspname = '{self._schema}'
		                    AND c.relname = '{self._name}'
		                    AND c.relkind = 'r'
                    ),
                    agg AS (
	                    SELECT rows.table_name, json_agg(rows ORDER BY attribute_num) AS attrs
	                    FROM rows
	                    GROUP BY rows.table_name
                    )
                    SELECT json_object_agg(agg.table_name, agg.attrs)
                    FROM agg;
                """
                logger.info(f"Fetching attributes of table {self._schema}.{self._name}")
                logger.debug(f"With query {sql_script}")

                fetch_result = cursor.execute(text(sql_script)).fetchone() or []
                # Current type: sqlalchemy.engine.row.Row
                fetch_result = fetch_result[0] or {}  # Current type: dict
                logger.debug(f"fetch_result: {fetch_result}")

                new_attributes = fetch_result.get(self.get_name()) or []
                logger.debug(f"new_attributes: {new_attributes}")

                if new_attributes == self._attributes:
                    logger.info("There's nothing to change")
                    return False
                else:
                    self.set_attributes(new_attributes)
                    logger.info("Table attributes are updated")
                    return True


def gen_public_test(connector: PsqlConnector, num_records: int = 1) -> None:
    for _ in range(num_records):
        with connector.connect() as engine:
            with engine.connect() as cursor:
                sql_script = f"""
                    INSERT INTO public.test
                        (name, address, zipcode, introduction)
                        VALUES ('{fake.name()}', '{fake.address()}', 
                                '{fake.zipcode()}', '{fake.text()}')
                """
                logger.info(f"Inserting query: {sql_script}")

                cursor.execute(text(sql_script))
                cursor.commit()
