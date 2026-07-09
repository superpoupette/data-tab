import requests
import streamlit as st


TMDB_API_KEY = st.secrets["TMDB_API_KEY"]


def get_movie_title(imdb_id):

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

    return movies[0].get("title")