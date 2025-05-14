import logging
import os

script_path = os.path.dirname(os.path.abspath(__file__))


def setup_logger(name="logs.log"):
    log_file = os.path.join(script_path, "../../log/logs.log")
    logging.basicConfig(
        level=logging.INFO,  # Niveau du logger (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        # Format message
        handlers=[
            logging.FileHandler(log_file),  # Enregistre les logs dans un fichier
            logging.StreamHandler(),  # Affiche les logs dans la console
        ],
    )
