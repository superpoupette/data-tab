import pandas as pd


def load_tvtime_movies(filepath):

    movies = pd.read_csv(filepath)

    return movies