from pathlib import Path
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from logging import getLogger

logger = getLogger(__name__)

# Chargement des variables d'environnement
script_path = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(script_path, "../../env/private.env")
load_dotenv(env_file)


def create_connection():
    try:
        mysql_user = os.getenv("MYSQL_USER")
        mysql_password = os.getenv("MYSQL_USER_PASSWORD")
        mysql_host = os.getenv("MYSQL_HOST")
        mysql_port = int(os.getenv("MYSQL_PORT", 3306))  # Default MySQL port
        mysql_database = os.getenv("MYSQL_DATABASE")

        logger.info(
            f"Attempting to connect to {mysql_host}:{mysql_port} as {mysql_user}"
        )

        sql_cmd = "mysql+pymysql"
        connection_string = f"{sql_cmd}://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
        engine = create_engine(connection_string)

        logger.info("Connection to MySQL established successfully.")
        return engine

    except SQLAlchemyError as e:
        logger.error(f"Error connecting to MySQL: {e}")
        return None


def insert_airports_into_mysql(engine, dataframe, table_name, column_mapping):
    try:
        # mapping cols
        df_sql = dataframe[list(column_mapping.keys())].rename(columns=column_mapping)

        df_sql = df_sql.dropna(subset=["airport_code"]).drop_duplicates(
            subset=["airport_code"]
        )

        df_sql.to_sql(name=table_name, con=engine, if_exists="append", index=False)

        logger.info(f"Data from {dataframe} inserted successfully into {table_name}")

    except Exception as e:
        logger.error(f"Error inserting data from CSV: {e}")
