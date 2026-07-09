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