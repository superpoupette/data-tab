import pandas as pd

def load_tv(filepath):
    tv = pd.read_csv(filepath)
    return tv


def tab_tv():
    movies=load_tv("data/tvtime-movies-2026-07-07.csv")
    series=load_tv("data/tvtime-series-2026-07-07.csv")
    series_episodes=load_tv("data/tvtime-series-episodes-2026-07-07.csv")
    return movies, series, series_episodes
