from scripts.import_data import load_movies
from scripts.cleaning import clean_movies
from scripts.enrichment import add_movie_rating, add_tmdb_info


def create_movies_dataset():

    movies = load_movies()

    movies = clean_movies(
        movies
    )

    movies = add_movie_rating(
        movies
    )

    movies = add_tmdb_info(
        movies
    )

    movies.to_csv(
        "data_cleaned/movies.csv",
        index=False
    )

    return movies