from sqlalchemy import text
from faker import Faker
from psql_connector import PsqlConnector

import os
import logging
from os import environ as env
from dotenv import load_dotenv


logger = logging.getLogger(__name__)
f_handler = logging.FileHandler(os.path.dirname(__file__) + f"/logs/{__name__}.log")
f_handler.setLevel(logging.DEBUG)
f_format = logging.Formatter("[ %(asctime)s - %(levelname)s - %(name)s ] %(message)s")
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)


load_dotenv()
psql_params = {
    "host": env["POSTGRES_HOST"],
    "port": env["POSTGRES_PORT"],
    "user": env["POSTGRES_USER"],
    "password": env["POSTGRES_PASSWORD"],
    "database": env["POSTGRES_DB"],
}


fake = Faker()


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


if __name__ == "__main__":
    psql_connector = PsqlConnector(psql_params)
    gen_public_test(connector=psql_connector, num_records=1)
