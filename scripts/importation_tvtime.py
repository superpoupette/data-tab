import pandas as pd


from scripts.tmdb import get_movie_info

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


    # Nombre total d'episodes disponibles
    episode_count = (
        series_episodes
        .groupby("series_uuid")
        .size()
        .reset_index(name="episodes")
    )


    # Nombre d'episodes rellement vus
    watched_count = (
        series_episodes[
            series_episodes["watched_at"].notna()
        ]
        .groupby("series_uuid")
        .size()
        .reset_index(name="progress")
    )


    # Fusion des deux informations
    episode_stats = episode_count.merge(
        watched_count,
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


    series["episodes"] = (
        series["episodes"]
        .fillna(0)
        .astype(int)
    )

    series["progress"] = (
        series["progress"]
        .fillna(0)
        .astype(int)
    )


    # Dernier episode regarde
    last_episode = (
        series_episodes[
            series_episodes["watched_at"].notna()
        ]
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


    last_episode = last_episode[
        ["series_uuid", "watched_at", "last_episode"]
    ].rename(
        columns={
            "watched_at": "last_watch"
        }
    )


    series = series.merge(
        last_episode,
        how="left",
        left_on="uuid",
        right_on="series_uuid"
    )


    series.drop(
        columns=["series_uuid"],
        inplace=True
    )


    return series


def add_movie_rating(movies):
    ratings = load_tv("data/ratings-live-votes.csv")

    ratings = ratings[
        ["uuid", "vote_key"]
    ]

    movies = movies.merge(
        ratings,
        on="uuid",
        how="left"
    )
    movies["vote_key"] = (
        movies["vote_key"]
        .str.split("-")
        .str[-1]
    )
    rating_map = {
        "1": 1,
        "27": 2,
        "28": 3,
        "29": 4,
        "3": 5
    }

    movies["rating"] = (
        movies["vote_key"]
        .map(rating_map)
    )

    return movies

def add_tmdb_info(movies):

    infos = []

    for _, movie in movies.iterrows():

        info = get_movie_info(
            movie["imdb_id"]
        )

        if info:
            info["uuid"] = movie["uuid"]
            infos.append(info)


    tmdb_df = pd.DataFrame(infos)


    movies = movies.merge(
        tmdb_df,
        on="uuid",
        how="left"
    )

    return movies

def tab_tv():
    movies = load_tv("data/tvtime-movies-2026-07-07.csv")
    series = load_tv("data/tvtime-series-2026-07-07.csv")
    series_episodes = load_tv("data/tvtime-series-episodes-2026-07-07.csv")

    movies = add_movie_rating(movies)
    movies = add_tmdb_info(movies)

    movies = clean_movies(movies)
    series = clean_series(series, series_episodes)

    return movies, series, series_episodes
