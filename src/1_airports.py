from dotenv import load_dotenv
from pathlib import Path
from dst_airlines.logging.log import setup_logger
from dst_airlines.load.mysql import (
    create_connection,
    insert_airports_into_mysql,
    airports_data_etl,
)
import pandas as pd
import sys

logger = setup_logger(__name__)

script_path = Path(__file__).parent.absolute()
env_file = script_path.parent / "env" / "private.env"
airports_csv = script_path.parent / "data" / "4_external" / "airport_names.csv"


def validate_dataframe(df, required_columns):
    """Valide le dataframe et ses colonnes requises"""
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")

    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    if df.empty:
        raise ValueError("DataFrame is empty")


def main():
    try:
        # Vérification des fichiers
        if not env_file.exists():
            raise FileNotFoundError(f"Environment file not found: {env_file}")

        if not airports_csv.exists():
            raise FileNotFoundError(f"CSV file not found: {airports_csv}")

        logger.info(f"Loading environment from: {env_file}")
        logger.info(f"Loading CSV from: {airports_csv}")

        # Chargement des variables d'environnement
        load_dotenv(env_file)

        # Connexion à la base de données
        connection = create_connection()
        if not connection:
            raise ConnectionError("Failed to connect to database")

        # Lecture et traitement des données
        table_name = "Airports"
        logger.info(f"Starting data import to table {table_name}")

        # Lecture du CSV
        airports_df = pd.read_csv(airports_csv)
        logger.info(f"CSV loaded successfully. Columns: {airports_df.columns.tolist()}")

        # Validation des colonnes requises dans le CSV original
        original_required_columns = [
            "iata_code",
            "name",
            "latitude_deg",
            "longitude_deg",
        ]
        validate_dataframe(airports_df, original_required_columns)

        # Renommage des colonnes pour correspondre aux noms attendus par le nettoyage
        airports_df = airports_df.rename(
            columns={
                "iata_code": "airport_code",
                "latitude_deg": "latitude",
                "longitude_deg": "longitude",
            }
        )

        # Vérification après renommage
        logger.info(f"Columns after renaming: {airports_df.columns.tolist()}")

        # Nettoyage des données
        airports_df = airports_data_etl(airports_df)

        logger.info(f"Data after cleaning:\n{airports_df.head()}")
        logger.info(f"Rows to insert: {len(airports_df)}")

        # Insertion en base - pas besoin de mapping car les noms correspondent déjà à ceux de la base
        insert_airports_into_mysql(connection, airports_df, table_name)

        logger.info(
            f"Successfully inserted {len(airports_df)} rows into {table_name} table"
        )
        logger.info("Data import completed successfully")

    except Exception as e:
        logger.error(f"Script failed: {str(e)}", exc_info=True)
        sys.exit(1)
    finally:
        if "connection" in locals() and connection:
            connection.close()
            logger.info("Database connection closed")


if __name__ == "__main__":
    main()
