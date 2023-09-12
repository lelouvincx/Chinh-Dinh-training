from sqlalchemy import text
import streamlit as st
from psql_connector import PsqlConnector

from os import environ as env
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

psql_params = {
    "host": "source_db",
    "port": env["POSTGRES_PORT"],
    "user": env["POSTGRES_USER"],
    "password": env["POSTGRES_PASSWORD"],
    "database": env["POSTGRES_DB"],
}

psql_connector = PsqlConnector(psql_params)


# Fetch schemas
schemas = []
with psql_connector.connect() as engine:
    with engine.connect() as cursor:
        print("Connected to database")
        sql_script = """
            SELECT schema_name
            FROM information_schema.schemata;
        """
        schemas = cursor.execute(text(sql_script)).fetchall()

# Init setup
st.set_page_config(
    page_title="Fake data generator",
    page_icon="🐧",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title(f"Fake data generator for {env['POSTGRES_DB']}")

# Generate x records for table
# st.header("Generate data")
# table = st.selectbox("Select table", ["users", "posts", "comments"])

st.write(schemas)
