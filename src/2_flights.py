from dst_airlines.logging.log import setup_logger
from pathlib import Path
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta
import dst_airlines.utils as utils
from dst_airlines.transform.flights_etl import download_fullday_departing_flights

logger = setup_logger(__name__)

script_path = Path(__file__).parent.absolute()
env_file = script_path.parent / "env" / "private.env"


def main():
    fra_iata = "FRA"

    # Récupération de l'adresse IP
    public_ip = utils.get_public_ip_address()

    # Récupération d'un token de l'API LH valide
    api_token = utils.get_lufthansa_token(user_id, secret)

    # Collecte des données d'il y a 3 jours (comportement par défaut quand la date et l'heure ne sont pas spécifiées) pour FRA
    download_fullday_departing_flights(
        api_token=api_token, public_ip=public_ip, airport_iata=fra_iata
    )


if __name__ == "__main__":
    load_dotenv(env_file)
    user_id = os.getenv("CLIENT_ID")
    secret = os.getenv("CLIENT_SECRET")
    main()
