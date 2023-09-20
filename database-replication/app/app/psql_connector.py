from sqlalchemy import create_engine
from contextlib import contextmanager

import os
import logging


# Init logging
logging.basicConfig(
    level=logging.INFO,
    format="[ %(name)s - %(asctime)s %(levelname)s ] %(message)s",
    handlers=[
        logging.FileHandler(os.path.dirname(__file__) + f"/logs/{__name__}.log"),
        logging.StreamHandler(),
    ],
)


class PsqlConnector:
    def __init__(self, params):
        self.params = params
        pass

    @contextmanager
    def connect(self):
        conn_info = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            self.params["user"],
            self.params["password"],
            self.params["host"],
            self.params["port"],
            self.params["database"],
        )
        db_conn = create_engine(conn_info)
        try:
            yield db_conn
        except Exception as e:
            logging.exception(f"Error when connecting to Postgres: {e}")
