import requests
import json
import logging
import argparse
from dotenv import load_dotenv
from os import environ as env


load_dotenv()

# Logging to console
logging.basicConfig(
    level=logging.INFO, format="[ %(asctime)s - %(levelname)s ] %(message)s"
)


def get_name(filename: str) -> str:
    with open(f"{filename}", "r") as json_file:
        json_tmp = json.load(json_file)
    name = json_tmp.get("name", "")

    if name == "":
        logging.error("Connector name not found. Please enter it in the config file.")
        raise Exception

    return name


def get_config(filename: str) -> dict:
    with open(f"{filename}", "r") as json_file:
        json_tmp = json.load(json_file)
    config = json_tmp.get("config")

    if config is None:
        logging.error("No config found. Please enter it in the config file.")
        raise Exception

    if config.get("io.debezium.connector.postgresql.PostgresConnector"):
        logging.warn(
            "The connector is not from io.debezium.connector.postgresql.PostgresConnector, some functionalities may not work"
        )

    config["database.hostname"] = "source_db"
    config["database.port"] = env["POSTGRES_PORT"] or "5432"
    config["database.user"] = env["POSTGRES_USER"]
    config["database.password"] = env["POSTGRES_PASSWORD"]
    config["database.dbname"] = env["POSTGRES_DB"]

    return config


def get_url(action: str, name: str) -> str:
    kafka_connect_host = env["CONNECT_REST_ADVERTISED_HOST_NAME"]
    kafka_connect_port = env["CONNECT_REST_PORT"]

    url = f"http://{kafka_connect_host}:{kafka_connect_port}/connectors"
    options = {
        "create": "",
        "update": f"/{name}/config",
        "restart": f"/{name}/restart",
        "show": f"/{name}",
        "list": f"/{name}/topics",
        "delete": f"/{name}",
    }
    url += options.get(action, "")

    return url


def make_request(action: str, filename: str) -> str:
    # Prepare url
    name = get_name(filename)
    url = get_url(action, name)
    logging.info(f"Endpoint: {url}")

    # Prepare headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    if action == "create" or action == "update":
        # Prepare json_data
        config = get_config(filename)

        json_data = (
            json.dumps({"name": name, "config": config})
            if action == "create"
            else json.dumps(config)  # action == "update"
        )

        # Make request
        try:
            response = (
                requests.post(url=url, data=json_data, headers=headers)
                if action == "create"
                else requests.put(url=url, data=json_data, headers=headers)
            )
            response.raise_for_status()

            logging.info("Request was successful")
            content = json.loads(response.content)
            content["config"][
                "database.password"
            ] = "********"  # WARN: Do not comment this line due to password security
            content["status_code"] = response.status_code
            formatted_json = json.dumps(content, indent=4)
            return formatted_json
        except requests.exceptions.HTTPError as e:
            logging.exception(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            logging.exception(f"POST or PUT request failed due to: {e}")
    elif action == "restart":
        # Make request
        try:
            response = requests.post(url=url, headers=headers)
            response.raise_for_status()

            if response.status_code == 204:
                logging.info("Restarted. Status code 204 No Content")
        except requests.exceptions.HTTPError as e:
            logging.exception(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            logging.exception(f"POST request failed due to: {e}")
    elif action == "show":
        # Make request
        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()

            logging.info("Request was successful")
            content = json.loads(response.content)
            content["config"][
                "database.password"
            ] = "********"  # WARN: Do not comment this line due to password security
            content["status_code"] = response.status_code
            formatted_json = json.dumps(content, indent=4)
            return formatted_json
        except requests.exceptions.HTTPError as e:
            logging.exception(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            logging.exception(f"GET request failed due to: {e}")
    elif action == "list":
        # Make request
        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()

            logging.info("Request was successful")
            content = json.loads(response.content)
            content["status_code"] = response.status_code
            formatted_json = json.dumps(content, indent=4)
            return formatted_json
        except requests.exceptions.HTTPError as e:
            logging.exception(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            logging.exception(f"GET request failed due to: {e}")
    else:  # action = "delete"
        # Make request
        try:
            response = requests.delete(url=url, headers=headers)
            response.raise_for_status()

            if response.status_code == 204:
                logging.info("Restarted. Status code 204 No Content")
        except requests.exceptions.HTTPError as e:
            logging.exception(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            logging.exception(f"DELETE request failed due to: {e}")

    return ""


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--action",
        choices=["create", "update", "restart", "show", "list", "delete"],
        default="update",
        help="Choose one: create/update/delete/restart/show/list",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        required=True,
        help="Provide path to config file. Example: connectors/source-db.json",
    )
    args = parser.parse_args()

    result = make_request(action=args.action, filename=args.config)
    logging.info(f"Content \n{result}")
