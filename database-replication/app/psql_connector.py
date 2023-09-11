from sqlalchemy import create_engine
from contextlib import contextmanager

from os import environ as env
from dotenv import load_dotenv
load_dotenv()

import logging
logger = logging.getLogger(__name__)
f_handler = logging.FileHandler(f"logs/{__name__}.log")
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s ] %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)


class PsqlConnector():
    def __init__(self, params):
        self.params = params
        pass

    @contextmanager
    def connect():
        conn_info = "postgresql+psycopg2://{}:{}@{}:{}/".format(
            env['POSTGRES_USER'],
            env['POSTGRES_PASSWORD'],
            env['POSTGRES_HOST'],
            env['POSTGRES_PORT'],
            env['POSTGRES_DB']
        )
        logging.info(f"Creating config string: {conn_info}")
        db_conn = create_engine(conn_info)
        try:
            yield db_conn
        except Exception as e:
            logging.exception(f"Error when connecting to Postgres: {e}")
