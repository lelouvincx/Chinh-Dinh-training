from sqlalchemy import text
from faker import Faker
from psql_connector import PsqlConnector

import os
import logging
logger = logging.getLogger(__name__)
f_handler = logging.FileHandler(os.path.dirname(__file__) + f"/logs/{__name__}.log")
f_handler.setLevel(logging.DEBUG)
f_format = logging.Formatter('[ %(asctime)s - %(levelname)s - %(name)s ] %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)


psql_params.host = "localhost"
psql_connector = PsqlConnector(psql_params)
fake = Faker()


def gen_public_test(num_records: int) -> None:
    for _ in range(num_records):
        with psql_connector.connect() as engine:
            with engine.connect() as cursor:
                sql_script = f"""
                    INSERT INTO public.test
                        (name, address, zipcode, introduction)
                        VALUES ('{fake.name()}', '{fake.address()}', '{fake.zipcode()}', '{fake.text()}')
                """
                logger.info(f"Inserting query: {sql_script}")

                cursor.execute(text(sql_script))
                cursor.commit()


if __name__ == "__main__":
    gen_public_test(1)
