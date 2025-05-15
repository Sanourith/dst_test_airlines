import pandas as pd


def transform_airports_data(csv_file):
    df_airports = pd.read_csv(csv_file)
    df = df_airports.dropna()
    df_sql = df[["iata_code", "latitude_deg", "longitude_deg", "name"]]
    return df_sql
