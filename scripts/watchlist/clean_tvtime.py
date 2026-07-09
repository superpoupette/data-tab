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