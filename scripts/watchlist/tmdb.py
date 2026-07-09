import requests
import pandas as pd
import streamlit as st


TMDB_API_KEY = st.secrets["TMDB_API_KEY"]


GENRES_FR = {
    "Action": "Action",
    "Adventure": "Aventure",
    "Animation": "Animation",
    "Comedy": "Comédie",
    "Crime": "Policier",
    "Documentary": "Documentaire",
    "Drama": "Drame",
    "Family": "Famille",
    "Fantasy": "Fantastique",
    "History": "Historique",
    "Horror": "Horreur",
    "Music": "Musique",
    "Mystery": "Mystère",
    "Romance": "Romance",
    "Science Fiction": "Science-fiction",
    "TV Movie": "Téléfilm",
    "Thriller": "Thriller",
    "War": "Guerre",
    "Western": "Western"
}


def get_movie_info(imdb_id):

    if pd.isna(imdb_id):
        return None

    url = (
        f"https://api.themoviedb.org/3/find/{imdb_id}"
        f"?api_key={TMDB_API_KEY}"
        "&external_source=imdb_id"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    movies = data.get("movie_results", [])

    if not movies:
        return None

    tmdb_id = movies[0]["id"]

    details = requests.get(
        f"https://api.themoviedb.org/3/movie/{tmdb_id}",
        params={
            "api_key": TMDB_API_KEY,
            "append_to_response": "credits"
        }
    ).json()

    director = None

    for person in details.get("credits", {}).get("crew", []):

        if person["job"] == "Director":
            director = person["name"]
            break

    countries = [
        c["name"]
        for c in details.get("production_countries", [])
    ]

    genres = [
        GENRES_FR.get(g["name"], g["name"])
        for g in details.get("genres", [])
    ]

    return {
        "director": director,
        "style": ", ".join(genres),
        "country": ", ".join(countries),
        "overview": details.get("overview"),
        "poster_path": details.get("poster_path"),
        "tmdb_rating": details.get("vote_average")
    }


def add_tmdb_info(movies):

    infos = []

    for _, movie in movies.iterrows():

        info = get_movie_info(movie["imdb_id"])

        if info:
            info["imdb_id"] = movie["imdb_id"]
            infos.append(info)

    tmdb_df = pd.DataFrame(infos)

    movies = movies.merge(
        tmdb_df,
        on="imdb_id",
        how="left"
    )

    return movies