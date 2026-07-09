from scripts.tvtime.import_tvtime import load_tvtime_movies
from scripts.tvtime.clean_tvtime import clean_movies
from scripts.tvtime.tmdb import add_tmdb_info
from scripts.tvtime.google_sheet import save_movies_google_sheet



def update_movies():


    movies = load_tvtime_movies(
        "data/tvtime-movies.csv"
    )


    movies = clean_movies(
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