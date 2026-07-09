import requests
import streamlit as st


TMDB_API_KEY = st.secrets["TMDB_API_KEY"]


def get_movie_info(imdb_id):

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

    movie = movies[0]

    tmdb_id = movie["id"]

    details_url = (
        f"https://api.themoviedb.org/3/movie/{tmdb_id}"
        f"?api_key={TMDB_API_KEY}"
        "&append_to_response=credits"
    )

    details = requests.get(details_url).json()


    director = None

    for person in details.get("credits", {}).get("crew", []):
        if person["job"] == "Director":
            director = person["name"]
            break


    countries = [
        country["name"]
        for country in details.get("production_countries", [])
    ]


    return {
        "release_date": details.get("release_date"),
        "director": director,
        "country": ", ".join(countries),
        "overview": details.get("overview"),
        "poster_path": details.get("poster_path"),
        "tmdb_rating": details.get("vote_average")
    }