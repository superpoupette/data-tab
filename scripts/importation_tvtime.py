import pandas as pd

def load_tv(filepath):
    tv = pd.read_csv(filepath)
    return tv

def clean_movies(movies):
    movies["type"] = "movie"
    return movies

def clean_series(series):
    series["type"] = "series"
    return series


def tab_tv():
    movies=load_tv("data/tvtime-movies-2026-07-07.csv")
    series=load_tv("data/tvtime-series-2026-07-07.csv")
    series_episodes=load_tv("data/tvtime-series-episodes-2026-07-07.csv")
    movies = clean_movies(movies)
    series = clean_series(series)
    return movies, series, series_episodes
