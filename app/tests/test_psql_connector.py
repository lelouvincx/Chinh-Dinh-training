from app.psql_connector import PsqlConnector
from conftest import psql_params
from sqlalchemy import text
import pytest


class TestPsqlConnector:
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
    def test_getting_data(self):
        psql_connector = PsqlConnector(psql_params)
        with psql_connector.connect() as engine:
            with engine.connect() as cursor:
                sql_script = "SELECT 1;"
                fetched_data = 0
                try:
                    fetched_data = cursor.execute(text(sql_script)).fetchone() or []
                    fetched_data = fetched_data[0] or int
                except Exception as e:
                    print(f"Error when retrieving results from database: {e}")
                    assert False, "Error when retrieving results."
                assert fetched_data == 1
