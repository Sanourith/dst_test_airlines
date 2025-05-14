import os
from pathlib import Path
from dotenv import load_dotenv
import pymysql

script_path = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(script_path, "../env/private.env")
load_dotenv(env_file)

airports_csv = os.path.join(script_path, "../data/4_external/airport_names.csv")

# TODO CONNEXION DATABASE
