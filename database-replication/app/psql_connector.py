from sqlalchemy import create_engine
from contextlib import contextmanager

import os
from os import environ as env
from dotenv import load_dotenv
load_dotenv()

import logging
logger = logging.getLogger(__name__)
f_handler = logging.FileHandler(os.path.dirname(__file__) + f"/logs/{__name__}.log")
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s ] %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)


class PsqlConnector():
    def __init__(self, params):
        self.params = params
        pass

    @contextmanager
    def connect(self):
        conn_info = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            self.params['user'],
            self.params['password'],
            self.params['host'],
            self.params['port'],
            self.params['database']
        )
        logging.info(f"Creating config string: {conn_info}")
        db_conn = create_engine(conn_info)
        try:
            yield db_conn
        except Exception as e:
            logging.exception(f"Error when connecting to Postgres: {e}")
            logger.exception(f"Error when connecting to Postgres: {e}")
