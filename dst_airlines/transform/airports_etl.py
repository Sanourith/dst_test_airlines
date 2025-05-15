import pandas as pd


def transform_airports_data(csv_file):
    df_airports = pd.read_csv(csv_file)
    df = df_airports.dropna()
