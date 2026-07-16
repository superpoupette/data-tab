import pandas as pd


def clean_movies(movies):

    movies = movies.copy()

    movies["type"] = "movie"

    movies["status"] = movies["is_watched"].apply(
        lambda x: "watched" if x else "to_watch"
    )

    movies["watched_at"] = pd.to_datetime(
        movies["watched_at"],
        errors="coerce"
    )

    movies.drop(
        columns=["is_watched"],
        inplace=True
    )

    return movies


def add_movie_rating(movies):

    ratings = pd.read_csv(
        "data/ratings-live-votes.csv"
    )

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
        .astype(str)
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


def clean_series(
    series,
    series_episodes
):

    series = series.copy()
    series_episodes = series_episodes.copy()

    series["type"] = "series"

    series["status"] = (
        series["status"]
        .replace(
            "not_started_yet",
            "to_watch"
        )
    )

    series_episodes["watched_at"] = pd.to_datetime(
        series_episodes["watched_at"],
        errors="coerce"
    )

    episode_count = (
        series_episodes
        .groupby("series_uuid")
        .size()
        .reset_index(name="episodes")
    )

    watched_count = (
        series_episodes[
            series_episodes["watched_at"].notna()
        ]
        .groupby("series_uuid")
        .size()
        .reset_index(name="progress")
    )

    series = series.merge(
        episode_count,
        left_on="uuid",
        right_on="series_uuid",
        how="left"
    )

    series = series.merge(
        watched_count,
        left_on="uuid",
        right_on="series_uuid",
        how="left",
        suffixes=("", "_watched")
    )

    series.drop(
        columns=[
            c
            for c in series.columns
            if c.startswith("series_uuid")
        ],
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
        + last_episode["season"]
        .astype(int)
        .astype(str)
        .str.zfill(2)
        + "E"
        + last_episode["episode"]
        .astype(int)
        .astype(str)
        .str.zfill(2)
    )

    last_episode = last_episode.rename(
        columns={
            "watched_at": "last_watch"
        }
    )

    series = series.merge(
        last_episode[
            [
                "series_uuid",
                "last_watch",
                "last_episode"
            ]
        ],
        left_on="uuid",
        right_on="series_uuid",
        how="left"
    )


    series.drop(
        columns=["series_uuid"],
        inplace=True
    )
    
    # Premier épisode regardé
    first_episode = (
        series_episodes[
            series_episodes["watched_at"].notna()
        ]
        .groupby("series_uuid")["watched_at"]
        .min()
        .reset_index()
        .rename(
            columns={
                "watched_at": "first_seen"
            }
        )
    )


    series = series.merge(
        first_episode,
        left_on="uuid",
        right_on="series_uuid",
        how="left"
    )


    series.drop(
        columns=["series_uuid"],
        inplace=True
    )

    return series


def clean_animes(animes):

    animes = animes.copy()

    animes["type"] = "anime"

    animes["status"] = (
        animes["status"]
        .replace(
            {
                "Completed": "watched",
                "Watching": "continuing",
                "Plan to Watch": "to_watch",
                "On-Hold": "paused",
                "Dropped": "stopped"
            }
        )

    animes["year"] = pd.NA
    animes["first_seen"] = pd.NaT
    animes["last_watch"] = pd.NaT
    animes["last_episode"] = pd.NA

    return animes