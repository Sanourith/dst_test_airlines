import os
from dotenv import load_dotenv
from dst_airlines.database.mysql import create_connection, insert_data_from_csv
from dst_airlines.
from pathlib import Path
from dst_airlines.logging.log import setup_logger

logger = setup_logger(__name__)

script_path = Path(__file__).parent.absolute()
env_file = script_path.parent / "env" / "private.env"
airports_csv = script_path.parent / "data" / "4_external" / "airport_names.csv"


def main():
    if not env_file.exists():
        logger.error(f"Environment file not found: {env_file}")
        return

    if not airports_csv.exists():
        logger.error(f"CSV file not found: {airports_csv}")
        return

    load_dotenv(env_file)

    connection = create_connection()
    if not connection:
        logger.error("Failed to connect to database")
        return

    try:
        table_name = "Airports"
        logger.info(f"Starting data import from {airports_csv} to table {table_name}")

        insert_data_from_csv(connection, str(airports_csv), table_name)

        logger.info("Data import completed successfully")
    except Exception as e:
        logger.error(f"An error occurred during data import: {e}")
    finally:
        if connection:
            connection.close()
            logger.info("Database connection closed")


if __name__ == "__main__":
    main()
