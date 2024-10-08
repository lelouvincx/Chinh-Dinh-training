from app.psql_connector import PsqlConnector
from app.gen_data import Table
from conftest import psql_params
from sqlalchemy import text
import pytest


class TestTable:
    @pytest.mark.first
    @pytest.mark.dependency(name="TEST_CONNECTING")
    def test_connecting(self):
        psql_connector = PsqlConnector(psql_params)
        is_connected = False
        with psql_connector.connect() as engine:
            with engine.connect() as cursor:
                is_connected = True
                cursor.commit()
        assert is_connected is True, "Not connected to database."

    @pytest.mark.dependency(depends=["TEST_CONNECTING"])
    def test_update_attributes(self):
        psql_connector = PsqlConnector(psql_params)

        with psql_connector.connect() as engine:
            with engine.connect() as cursor:
                # Create temp_table
                sql_script = text(
                    """
                    CREATE TABLE temp_table (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(50),
                        age INT
                    );
                """
                )
                cursor.execute(sql_script)
                cursor.commit()

                # Find schema of temp_table
                sql_script = text(
                    """
                    SELECT schemaname
                    FROM pg_tables
                    WHERE tablename = 'temp_table';
                """
                )
                temp_table_schema = cursor.execute(sql_script).fetchone() or []
                temp_table_schema = temp_table_schema[0]

        # Check if attributes are updated
        temp_table = Table(schema=temp_table_schema, name="temp_table")
        is_changed = temp_table.update_attributes(psql_connector)

        # Clean created table
        with psql_connector.connect() as engine:
            with engine.connect() as cursor:
                sql_script = text(" DROP TABLE temp_table; ")
                cursor.execute(sql_script)
                cursor.commit()

        assert is_changed is True, "Attributes not changed."

    @pytest.mark.skip(reason="Not implemented due to WIP")
    @pytest.mark.dependency(depends=["TEST_CONNECTING"])
    def test_generate(self):
        pass
