from pathlib import Path
import os
import pymysql
import pandas as pd
from logging import getLogger

logger = getLogger(__name__)


def create_connection():
    """Crée une connexion à la base de données MySQL avec PyMySQL"""
    try:
        sql_user = os.getenv("MYSQL_USER")
        sql_pwd = os.getenv("MYSQL_USER_PASSWORD")
        sql_host = os.getenv("MYSQL_HOST")
        sql_port = int(os.getenv("MYSQL_PORT", "3306"))
        sql_db = os.getenv("MYSQL_DATABASE")

        if not all([sql_user, sql_pwd, sql_host, sql_db]):
            raise ValueError("Missing required database connection parameters")

        logger.info(f"Attempting to connect to {sql_host}:{sql_port} as {sql_user}")

        connection = pymysql.connect(
            host=sql_host,
            user=sql_user,
            password=sql_pwd,
            database=sql_db,
            port=sql_port,
            charset="utf8mb4",
        )

        logger.info("Connexion MySQL établie avec succès")
        return connection

    except Exception as e:
        logger.error(f"Erreur de connexion à MySQL : {str(e)}", exc_info=True)
        return None


def airports_data_etl(df):
    """Nettoie les données des aéroports"""
    try:
        if not isinstance(df, pd.DataFrame):
            raise ValueError("L'input doit être un DataFrame pandas")

        required_cols = ["airport_code", "name", "latitude", "longitude"]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Colonnes manquantes : {missing}")

        # Nettoyage
        df_clean = df.dropna()
        df_clean = df_clean.dropna(subset=["airport_code"])
        print("\n\n\n\n DUPS : ")
        duplicates = df_clean[df_clean.duplicated(subset=["airport_code"], keep=False)]
        print(duplicates)
        df_clean = df_clean.drop_duplicates(subset=["airport_code"])

        logger.info(f"Nettoyage terminé. Lignes restantes : {len(df_clean)}")
        return df_clean

    except Exception as e:
        logger.error(f"Erreur lors du nettoyage : {str(e)}", exc_info=True)
        raise


def insert_airports_into_mysql(connection, dataframe, table_name, column_mapping=None):
    """Insertion optimisée avec PyMySQL"""
    try:
        if not isinstance(dataframe, pd.DataFrame) or dataframe.empty:
            raise ValueError("DataFrame vide ou invalide")

        # Vérification des colonnes
        required_cols = ["airport_code", "name", "latitude", "longitude"]
        missing = [col for col in required_cols if col not in dataframe.columns]
        if missing:
            raise ValueError(f"Colonnes requises manquantes : {missing}")

        # Utiliser directement le DataFrame tel qu'il est (les colonnes sont déjà correctes)
        df_to_insert = dataframe[required_cols].copy()

        logger.info(f"Colonnes à insérer : {df_to_insert.columns.tolist()}")

        # Insertion par lots
        with connection.cursor() as cursor:
            for _, row in df_to_insert.iterrows():
                sql = f"""
                INSERT INTO {table_name} (airport_code, name, latitude, longitude)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(
                    sql,
                    (
                        row["airport_code"],
                        row["name"],
                        row["latitude"],
                        row["longitude"],
                    ),
                )

        connection.commit()
        logger.info(f"Insertion réussie de {len(dataframe)} lignes")

    except pymysql.Error as e:
        logger.error(f"Erreur SQL : {str(e)}", exc_info=True)
        connection.rollback()
        raise
    except Exception as e:
        logger.error(f"Erreur inattendue : {str(e)}", exc_info=True)
        connection.rollback()
        raise
