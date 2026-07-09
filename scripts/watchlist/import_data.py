import pandas as pd


def load_movies():
    return pd.read_csv(
        "data/raw/tvtime-movies.csv"
    )


def load_series():
    return pd.read_csv(
        "data/raw/tvtime-series.csv"
    )


def load_series_episodes():
    return pd.read_csv(
        "data/raw/tvtime-series-episodes.csv"
    )