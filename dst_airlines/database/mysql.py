from pathlib import Path
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from logging import getLogger

logger = getLogger(__name__)

script_path = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(script_path, "../../env/private.env")
load_dotenv(env_file)


def create_connection():
    try:
        mysql_user = os.getenv("MYSQL_USER")
        mysql_password = os.getenv("MYSQL_USER_PASSWORD")
        mysql_host = os.getenv("MYSQL_HOST")
        mysql_port = os.getenv("MYSQL_PORT")
        mysql_database = os.getenv("MYSQL_DATABASE")
        # si besoin, root user avec root_password

        sql_cmd = "mysql+pymysql://"
        connection_string = f"{sql_cmd}{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"

        logger.info(
            f"Attempting to connect to {mysql_host}:{mysql_port} as {mysql_user}"
        )
        engine = create_engine(connection_string)

        with engine.connect() as conn:
            pass
        logger.info("Connection to MySQL established successfully.")
        return engine

    except SQLAlchemyError as e:
        logger.error(f"Error connecting MySQL : {e}")
        return None


create_connection()
