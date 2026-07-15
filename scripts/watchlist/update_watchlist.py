from scripts.watchlist.import_tvtime import (
    load_tvtime_movies,
    load_tvtime_series,
    load_tvtime_series_episodes
)

from scripts.watchlist.clean_tvtime import (
    clean_movies,
    clean_series,
    add_movie_rating
)

from scripts.watchlist.tmdb import add_tmdb_info

from scripts.watchlist.google_sheet import (
    save_movies_google_sheet
)

import gspread
import streamlit as st

from google.oauth2.service_account import Credentials


SHEET_ID = "1r-cWFbD68vRs3FNTeI3w11Dq--ZeucvMvRKbrq9k24A"


def get_movie_sheet():

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ]
    )

    client = gspread.authorize(
        credentials
    )

    return client.open_by_key(
        SHEET_ID
    ).sheet1


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

    save_movies_google_sheet(
        movies
    )

    return movies


def update_series():

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

    columns = [
        "tvdb_id",
        "title",
        "year",
        "status",
        "type",
        "episodes",
        "progress",
        "last_episode",
        "last_watch"
    ]

    series = series.reindex(
        columns=columns
    )

    return series


def add_movie_google_sheet(
    movie,
    watched_at,
    rating
):

    sheet = get_movie_sheet()

    row = [
        str(movie.get("tvdb_id", "")),
        str(movie.get("imdb_id", "")),
        str(movie.get("title", "")),
        str(movie.get("year", "")),
        str(movie.get("director", "")),
        str(watched_at),
        float(rating),
        "movie",
        "watched",
        str(movie.get("style", "")),
        str(movie.get("country", "")),
        str(movie.get("overview", "")),
        str(movie.get("poster_path", "")),
        float(movie.get("tmdb_rating", 0))
        if movie.get("tmdb_rating")
        else ""
    ]

    if len(row) != 14:
        raise ValueError(
            f"Erreur : {len(row)} colonnes envoyées au lieu de 14"
        )

    sheet.append_row(
        row,
        value_input_option="USER_ENTERED"
    )