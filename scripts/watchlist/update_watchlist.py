from scripts.watchlist.import_tvtime import load_tvtime_movies
from scripts.watchlist.clean_tvtime import (
    clean_movies,
    add_movie_rating
    )
from scripts.watchlist.tmdb import add_tmdb_info
from scripts.watchlist.google_sheet import save_movies_google_sheet

import gspread
import streamlit as st

from google.oauth2.service_account import Credentials

SHEET_ID = "1r-cWFbD68vRs3FNTeI3w11Dq--ZeucvMvRKbrq9k24A"

def update_movies():


    movies = load_tvtime_movies(
        "data/tvtime-movies-2026-07-07.csv"
    )


    movies = clean_movies(
        movies
    )
    movies = add_movie_rating(movies)

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

def add_movie_google_sheet(
    title,
    watched_at,
    rating
):

    sheet = get_movie_sheet()


    row = [
        "",                 # tvdb_id
        "",                 # imdb_id
        title,              # title
        "",                 # year
        "",                 # director
        watched_at,         # watched_at
        rating,             # rating
        "movie",            # type
        "watched",          # status
        "",                 # style
        "",                 # country
        "",                 # overview
        "",                 # poster_path
        ""                  # tmdb_rating
    ]


    sheet.append_row(row)