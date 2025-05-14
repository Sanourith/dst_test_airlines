import os
from pathlib import Path
from dotenv import load_dotenv
import pymysql
from dst_airlines.database.mysql import create_connection, insert_data_from_csv


script_path = os.path.dirname(os.path.abspath(__file__))

env_file = os.path.join(script_path, "../env/private.env")
airports_csv = os.path.join(script_path, "../data/4_external/airport_names.csv")


def main():
    table_name = "airports"

    engine = create_connection()
    if engine:
        insert_data_from_csv(engine, airports_csv, table_name)


if __name__ == "__main__":
    load_dotenv(env_file)
    main()
