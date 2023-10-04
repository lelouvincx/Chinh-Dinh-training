import json, requests
import argparse
from dotenv import load_dotenv
from os import environ as env


load_dotenv()


with open("connectors/source-db.json", "r") as json_file:
    config = json.load(json_file)
    config = config.get("config")

config["database.hostname"] = "source_db"
config["database.port"] = env["POSTGRES_PORT"] or "5432"
config["database.user"] = env["POSTGRES_USER"]
config["database.password"] = env["POSTGRES_PASSWORD"]
config["database.dbname"] = env["POSTGRES_DB"]


def make_request(action: str) -> str:
    # Prepare url
    if action == "create":
        url = "http://localhost:8083/connectors"
    elif action == "update":
        url = "http://localhost:8083/connectors/source-db-connector/config"
    else:  # action = "delete"
        url = "http://localhost:8083/connectors/source-db-connector"

    # Prepare headers
    headers = {"Content-Type": "application/json"}

    if action == "create" or action == "update":
        # Prepare json_data
        with open("connectors/source-db.json", "r") as json_file:
            json_tmp = json.load(json_file)

        name = json_tmp.get("name")
        config = json_tmp.get("config")

        config["database.hostname"] = "source_db"
        config["database.port"] = env["POSTGRES_PORT"] or "5432"
        config["database.user"] = env["POSTGRES_USER"]
        config["database.password"] = env["POSTGRES_PASSWORD"]
        config["database.dbname"] = env["POSTGRES_DB"]

        json_data = (
            json.dumps({"name": name, "config": config})
            if action == "create"
            else json.dumps(config)
        )

        # Make request
        try:
            response = (
                requests.post(url=url, data=json_data, headers=headers)
                if action == "create"
                else requests.put(url=url, data=json_data, headers=headers)
            )
            response.raise_for_status()
            content = json.loads(response.content)
            # WARN: Do not comment this line due to password security
            content["config"]["database.password"] = "********"
            content["status_code"] = response.status_code
            formatted_json = json.dumps(content, indent=4)
            return formatted_json
        except requests.exceptions.RequestException as e:
            print(f"POST or PUT request failed due to: {e}")
    else:  # action = "delete"
        # Make request
        try:
            response = requests.delete(url=url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"DELETE request failed due to: {e}")

    return ""


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--action",
        choices=["create", "update", "delete"],
        default="update",
        help="Choose 1: create/update/delete.",
    )
    args = parser.parse_args()

    result = make_request(action=args.action)
    print(result)
