from scripts.watchlist.import_tvtime import (
    load_tvtime_movies,
    load_tvtime_series,
    load_tvtime_series_episodes,
    load_myanimelist
)

from scripts.watchlist.clean_tvtime import (
    clean_movies,
    clean_series,
    clean_animes,
    add_movie_rating
)

from scripts.watchlist.tmdb import (
    add_tmdb_info,
    add_tmdb_series_info
)

from scripts.watchlist.google_sheet import (
    save_google_sheet
)

import pandas as pd


def update_movies():

    movies = load_tvtime_movies(
        "data/tvtime-movies-2026-07-07.csv"
    )

    movies = clean_movies(
        movies
    )

    movies = add_movie_rating(
        movies
    )

    movies = add_tmdb_info(
        movies
    )

    columns = [
        "tvdb_id",
        "imdb_id",
        "title",
        "year",
        "director",
        "watched_at",
        "rating",
        "type",
        "status",
        "style",
        "country",
        "overview",
        "poster_path",
        "tmdb_rating"
    ]

    movies = movies.reindex(
        columns=columns
    )

    save_google_sheet(
        movies,
        "movies"
    )

    return movies


def update_series():

    # ======================
    # TV Time
    # ======================

    series = load_tvtime_series(
        "data/tvtime-series-2026-07-07.csv"
    )

    episodes = load_tvtime_series_episodes(
        "data/tvtime-series-episodes-2026-07-07.csv"
    )

    series = clean_series(
        series,
        episodes
    )

    # Enrichissement TMDB
    series = add_tmdb_series_info(
        series
    )

    # ======================
    # MyAnimeList
    # ======================

    animes = load_myanimelist(
        "data/animelist.xml"
    )

    animes = clean_animes(
        animes
    )

    # Enrichissement TMDB
    animes = add_tmdb_series_info(
        animes
    )

    # ======================
    # Colonnes finales
    # ======================

    columns = [
        "tvdb_id",
        "title",
        "year",
        "status",
        "type",
        "episodes",
        "progress",
        "first_seen",
        "last_episode",
        "last_watch",
        "style",
        "country",
        "overview",
        "poster_path",
        "tmdb_rating"
    ]

    series = series.reindex(
        columns=columns
    )

    animes = animes.reindex(
        columns=columns
    )

    # ======================
    # Fusion
    # ======================

    series = pd.concat(
        [
            series,
            animes
        ],
        ignore_index=True
    )

    save_google_sheet(
        series,
        "series"
    )

    return series