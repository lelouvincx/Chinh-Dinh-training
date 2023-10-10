from os.path import dirname, abspath
import sys

parent_dir = dirname(dirname(abspath(__file__)))
sys.path.append(parent_dir)

from dotenv import load_dotenv
from os import environ as env

try:
    load_dotenv()
except Exception as e:
    pass


psql_params = {
    "host": env["POSTGRES_HOST"],
    "port": env["POSTGRES_PORT"],
    "user": env["POSTGRES_USER"],
    "password": env["POSTGRES_PASSWORD"],
    "database": env["POSTGRES_DB"],
}
