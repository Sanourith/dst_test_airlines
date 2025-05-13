from pathlib import Path
import os
from dotenv import load_dotenv

script_path = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(script_path, "../../env/private.env")
load_dotenv(env_file)
