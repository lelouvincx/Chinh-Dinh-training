import os
import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from psycopg2 import OperationalError

# Init logging
log_dir = os.path.dirname(__file__) + "/logs"
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format="[ %(name)s - %(asctime)s %(levelname)s ] %(message)s",
    handlers=[
        logging.FileHandler(log_dir + f"/{__name__}.log"),
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
        except OperationalError as e:
            logging.exception(f"Error when connecting to Postgres: {e}")
        finally:
            db_conn.dispose()
