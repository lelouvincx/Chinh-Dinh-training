# Config relative path to module app
from os.path import dirname, abspath
import sys

parent_dir = dirname(dirname(abspath(__file__)))
sys.path.append(parent_dir)


from app.psql_connector import PsqlConnector
from sqlalchemy import text
from dotenv import load_dotenv
from os import environ as env
import pytest

load_dotenv()

psql_params = {
    "host": env["POSTGRES_HOST"],
    "port": env["POSTGRES_PORT"],
    "user": env["POSTGRES_USER"],
    "password": env["POSTGRES_PASSWORD"],
    "database": env["POSTGRES_DB"],
}


@pytest.fixture
def create_temp_table():
    psql_connector = PsqlConnector(psql_params)

    # Create temp_table
    with psql_connector.connect() as engine:
        with engine.connect() as cursor:
            sql_script = text("""
                CREATE TEMP TABLE temp_table (
                    id serial PRIMARY KEY,
                    name VARCHAR(50),
                    age INT
                )
            """)
            cursor.execute(sql_script)
            cursor.commit()

    # Find schema of temp_table
    with psql_connector.connect() as engine:
        with engine.connect() as cursor:
            sql_script = text("""
                SELECT schemaname
                FROM pg_tables
                WHERE tablename = 'temp_table';
            """)
            temp_table_schema = cursor.execute(sql_script).fetchone() or []
            temp_table_schema = temp_table_schema[0] or str

    # Create Table object for temp_table
    return temp_table_schema
