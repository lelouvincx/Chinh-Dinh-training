from sqlalchemy.util import to_list
import streamlit as st
import pandas as pd
from sqlalchemy import text
from app.psql_connector import PsqlConnector

from gen_data import gen_public_test

from os import environ as env
from dotenv import load_dotenv
import logging
import time

load_dotenv(dotenv_path="../../.env")

# Init logging
logging.basicConfig(
    level=logging.NOTSET,
    format="[ %(name)s - %(asctime)s %(levelname)s ] %(message)s",
    handlers=[logging.FileHandler("./logs/streamlit.log"), logging.StreamHandler()],
)

# Init psql connector
psql_params = {
    "host": "source_db",
    "port": env["POSTGRES_PORT"],
    "user": env["POSTGRES_USER"],
    "password": env["POSTGRES_PASSWORD"],
    "database": env["POSTGRES_DB"],
}

psql_connector = PsqlConnector(psql_params)

# Init setup
st.set_page_config(
    page_title="Fake data generator",
    page_icon="🐧",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.title(f"Fake data generator for {env['POSTGRES_DB']}")


# Fetch schemas
schemas = []
with psql_connector.connect() as engine:
    with engine.connect() as cursor:
        logging.info("Connected to database")
        sql_script = """
            SELECT schema_name
            FROM information_schema.schemata;
        """
        schemas = cursor.execute(text(sql_script)).fetchall()
        # Remove system schemas
        schemas = [
            schema[0]
            for schema in schemas
            if schema[0]
            not in [
                "pg_toast",
                "pg_temp_1",
                "pg_toast_temp_1",
                "pg_catalog",
                "information_schema",
            ]
        ]
        # Remove schemas: data_load_simulation, integration, power_bi, reports, sequences
        schemas = [
            schema
            for schema in schemas
            if schema
            not in [
                "data_load_simulation",
                "integration",
                "power_bi",
                "reports",
                "sequences",
            ]
        ]

# Select schema
st_schema = st.selectbox("Select schema", schemas)


# Fetch tables from st_schema
tables = []
with psql_connector.connect() as engine:
    with engine.connect() as cursor:
        logging.debug("Connected to database")
        sql_script = f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = '{st_schema}';
        """
        tables = to_list(cursor.execute(text(sql_script)).fetchall())
        logging.debug(f"Tables type: {type(tables)}")
        # Remove outlines pattern for each table
        for table in tables:
            tables[tables.index(table)] = table[0]

# Select table
st_table = st.selectbox("Select table", tables)


# Option to view first 10 rows
if st.toggle("View first 10 rows"):
    with psql_connector.connect() as engine:
        with engine.connect() as cursor:
            logging.debug("Connected to database")
            sql_script = f"""
                SELECT *
                FROM {st_schema}.{st_table}
                LIMIT 10;
            """
            df = cursor.execute(text(sql_script)).fetchall()
            # Turn df to pandas.DataFrame
            df = pd.DataFrame(df)
            st.dataframe(df)
            sql_script = f"""
                SELECT COUNT(*)
                FROM {st_schema}.{st_table};
            """
            num_rows = cursor.execute(text(sql_script)).fetchall()[0][0]
            st.write(f"Total rows: {num_rows}")


# Option to input number of records to generate fake data
st_schema = "public"
st_table = "test"
st.write("## [Try] Generate fake data")
num_records = st.number_input("Number of records", min_value=1, max_value=10, value=1)
if st.button(f"Generate to {st_schema}.{st_table}"):
    gen_public_test(connector=psql_connector, num_records=int(num_records))


# Option to generate data through a period of time
st.write("## [Realtime] Generate fake data through a period of time")
period = st.number_input("Period (in seconds)", min_value=1, max_value=600, value=5)
num_records = st.number_input(
    "Number of records each time", min_value=1, max_value=10, value=1
)
times = st.number_input("Number of times", min_value=1, max_value=100, value=5)

st.write(
    f"Generating total {num_records * times} records to {st_schema}.{st_table} through"
    f" {period * times} seconds"
)
if st.button("Start generating"):
    for _ in range(int(times)):
        gen_public_test(connector=psql_connector, num_records=int(num_records))
        time.sleep(period)
