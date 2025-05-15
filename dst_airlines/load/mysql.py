from pathlib import Path
import os
from dotenv import load_dotenv
import pymysql
import pymysql.cursors
from logging import getLogger
import pandas as pd
import logging

logger = getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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

        connection = pymysql.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database,
            port=mysql_port,
            cursorclass=pymysql.cursors.DictCursor,
            charset="utf8mb4",
        )

        logger.info("Connection to MySQL established successfully.")
        return connection

    except pymysql.Error as e:
        logger.error(f"Error connecting to MySQL: {e}")
        return None


def insert_data_from_csv(connection, csv_file_path, table_name):
    try:
        df = pd.read_csv(csv_file_path)

        with connection.cursor() as cursor:
            columns = ", ".join([f"`{col}` TEXT" for col in df.columns])
            cursor.execute(f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns})")

            placeholders = ", ".join(["%s"] * len(df.columns))
            columns = ", ".join([f"`{col}`" for col in df.columns])
            sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"

            for _, row in df.iterrows():
                cursor.execute(sql, tuple(row))

            connection.commit()

        logger.info(
            f"Data from {csv_file_path} inserted successfully into {table_name}"
        )

    except Exception as e:
        connection.rollback()
        logger.error(f"Error inserting data from CSV: {e}")


def execute_query(connection, query, params=None):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            return result
    except pymysql.Error as e:
        logger.error(f"Error executing query: {e}")
        return None
