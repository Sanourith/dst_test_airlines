import requests
import json
from dst_airlines.logging.log import setup_logger
import os
import pandas as pd
from flatten_json import flatten

logger = setup_logger()


def get_project_root_path() -> str:
    """Return the absolute path to the root of the project

    Returns:
        str: Path to the project root
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    return project_root


def get_public_ip_address() -> str:
    """Get your public address via the website ipfy.org

    Returns:
        str: Your public IP
    """
    ipfy_url = "https://api.ipify.org?format=json"

    try:
        response = requests.get(ipfy_url)
        ip_info = response.json()
        public_ip = ip_info["ip"]
        return public_ip
    except requests.RequestException:
        logger.exception("Erreur de récupération de l'adresse IP")
        return None


def flatten_list_of_dict(dicts: list) -> pd.DataFrame:
    """Flatten a list of dictionaries into a pandas DataFrame

    Args:
        dicts (list): List of dictonaries to be flatten

    Returns:
        pd.DataFrame: Resulting flattened dataframe
    """
    return pd.DataFrame([flatten(d) for d in dicts])


def get_lufthansa_token(user_id, secret):
    url = "https://api.lufthansa.com/v1/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": user_id,
        "client_secret": secret,
        "grant_type": "client_credentials",
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]


def store_json_file(file_path: str, data: object) -> None:
    """Store data into a JSON file

    Args:
        file_path (str): Path where to store the data
        data (object): Data to be stored
    """
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
        logger.info(f"Données enregistrées dans '{file_path}'.")


def retrieve_json(file_path: str) -> dict | list:
    """Retrieve JSON data from the given file path

    Args:
        file_path (str): Path of the JSON to be retrieved

    Returns:
        dict | list: Dict or list of dicts stored into the JSON
    """
    try:
        with open(file_path, "r") as f:
            flight_data = json.load(f)
    except FileNotFoundError:
        logger.exception(f"Le fichier {f} n'a pas été trouvé.")
    except json.JSONDecodeError:
        logger.exception(f"Erreur de syntaxe dans le fichier JSON.")
    return flight_data


def build_data_storage_path(file_name: str, data_stage: str, folder: str = "") -> str:
    """Build an absolute path combining the given file name and the folder corresponding to the given data stage

    Args:
        file_name (str): Name of the file to be saved
        data_stage (str, optional): Name of the data stage. Defaults to "".
        folder (str): Name of the folder within the data_stage (e.g., "flights" or "weather_daily")

    Raises:
        ValueError: Error raised when the data_stage is not recognized or there is no corresponding folder to the given stage

    Returns:
        str: _description_
    """
    data_paths = {
        "raw": "1_raw",
        "interim": "2_interim",
        "processed": "3_processed",
        "external": "4_external",
    }

    if data_stage in data_paths:
        complete_data_stage = data_paths[data_stage]
    else:
        logger.error(
            f"Le stage '{data_stage}' n'est pas dans la liste des possibilités : {data_paths.keys}."
        )
        raise ValueError(
            f"Le stage '{data_stage}' n'est pas dans la liste des possibilités : {data_paths.keys}."
        )

    project_root = get_project_root_path()
    path = os.path.join(project_root, "data", complete_data_stage, folder)

    if not os.path.exists(path):
        logger.error(f"Le chemin '{path}' n'existe pas sur votre machine.")
        raise ValueError(f"Le chemin '{path}' n'existe pas sur votre machine.")
    else:
        return os.path.join(path, file_name)
