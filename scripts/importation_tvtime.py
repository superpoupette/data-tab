import pandas as pd

def load_tv(filepath):
    tv = pd.read_csv(filepath)
    return tv

def clean_movies(movies):
    movies["type"] = "movie"

    movies["status"] = movies["is_watched"].apply(
        lambda x: "watched" if x else "to_watch"
    )

    movies.drop(columns=["is_watched"], inplace=True)

    movies["watched_at"] = pd.to_datetime(
        movies["watched_at"],
        errors="coerce"
    )

    return movies

def clean_series(series, series_episodes):
    series["type"] = "series"

    series["status"] = series["status"].replace(
        "not_started_yet", "to_watch"
    )

    series_episodes["watched_at"] = pd.to_datetime(
        series_episodes["watched_at"],
        errors="coerce"
    )


    # Nombre d'épisodes vus + dernier épisode vu
    episode_stats = (
        series_episodes
        .sort_values("watched_at")
        .groupby("series_uuid")
        .agg(
            progress=("episode", "count"),
            last_watch=("watched_at", "max")
        )
        .reset_index()
    )


    last_episode = (
        series_episodes
        .sort_values("watched_at")
        .groupby("series_uuid")
        .last()
        .reset_index()
    )

    last_episode["last_episode"] = (
        "S"
        + last_episode["season"].astype(int).astype(str).str.zfill(2)
        + "E"
        + last_episode["episode"].astype(int).astype(str).str.zfill(2)
    )


    episode_stats = episode_stats.merge(
        last_episode[
            ["series_uuid", "last_episode"]
        ],
        on="series_uuid",
        how="left"
    )


    series = series.merge(
        episode_stats,
        how="left",
        left_on="uuid",
        right_on="series_uuid"
    )


    series.drop(
        columns=["series_uuid"],
        inplace=True
    )


    series["progress"] = (
        series["progress"]
        .fillna(0)
        .astype(int)
    )


    return series

def tab_tv():
    movies=load_tv("data/tvtime-movies-2026-07-07.csv")
    series=load_tv("data/tvtime-series-2026-07-07.csv")
    series_episodes=load_tv("data/tvtime-series-episodes-2026-07-07.csv")
    movies = clean_movies(movies)
    series = clean_series(series, series_episodes)
    return movies, series, series_episodes
