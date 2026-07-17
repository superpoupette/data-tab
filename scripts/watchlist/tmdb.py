# -*- coding: utf-8 -*-

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

def search_tmdb_series(query):

    url = "https://api.themoviedb.org/3/search/tv"

    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "language": "fr-FR"
    }

    response = requests.get(
        url,
        params=params
    )

    if response.status_code != 200:
        return None

    results = response.json().get(
        "results",
        []
    )

    if not results:
        return None

    tv = results[0]

    return get_series_details_tmdb(
        tv["id"]
    )



def get_series_details_tmdb(series_id):

    url = (
        f"https://api.themoviedb.org/3/tv/{series_id}"
    )


    response = requests.get(
        url,
        params={
            "api_key": TMDB_API_KEY,
            "language": "fr-FR"
        }
    )


    if response.status_code != 200:
        return None


    details = response.json()


    genres = [
        GENRES_FR.get(
            g["name"],
            g["name"]
        )
        for g in details.get(
            "genres",
            []
        )
    ]


    countries = [
        c
        for c in details.get(
            "origin_country",
            []
        )
    ]


    poster = ""

    if details.get("poster_path"):

        poster = (
            "https://image.tmdb.org/t/p/w500"
            + details["poster_path"]
        )


    return {

        "style": ", ".join(
            genres
        ),

        "country": ", ".join(
            countries
        ),

        "overview": details.get(
            "overview",
            ""
        ),

        "poster_path": poster,

        "tmdb_rating": details.get(
            "vote_average",
            ""
        )
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


def search_movies_tmdb(query):

    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "language": "fr-FR"
    }

    response = requests.get(
        url,
        params=params
    )

    results = response.json().get(
        "results",
        []
    )


    movies = []

    for movie in results[:10]:

        movies.append(
            {
                "id": movie["id"],
                "title": movie.get(
                    "title",
                    ""
                ),
                "year": movie.get(
                    "release_date",
                    ""
                )[:4],
                "overview": movie.get(
                    "overview",
                    ""
                ),
                "poster_path": (
                    "https://image.tmdb.org/t/p/w200"
                    + movie["poster_path"]
                )
                if movie.get("poster_path")
                else ""
            }
        )


    return movies

def get_movie_details_tmdb(movie_id):

    url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}"
    )


    response = requests.get(
        url,
        params={
            "api_key": TMDB_API_KEY,
            "language": "fr-FR",
            "append_to_response": "credits"
        }
    )


    details = response.json()


    director = ""

    for person in details.get(
        "credits",
        {}
    ).get(
        "crew",
        []
    ):

        if person.get("job") == "Director":
            director = person.get("name")
            break



    genres = [
        GENRES_FR.get(
            g["name"],
            g["name"]
        )
        for g in details.get(
            "genres",
            []
        )
    ]


    countries = [
        c["name"]
        for c in details.get(
            "production_countries",
            []
        )
    ]


    release_date = (
        details.get("release_date")
        or ""
    )


    poster = ""

    if details.get("poster_path"):

        poster = (
            "https://image.tmdb.org/t/p/w500"
            + details["poster_path"]
        )



    return {

        "imdb_id": details.get(
            "imdb_id",
            ""
        ),

        "title": details.get(
            "title",
            ""
        ),

        "year": release_date[:4],

        "director": director,

        "style": ", ".join(
            genres
        ),

        "country": ", ".join(
            countries
        ),

        "overview": details.get(
            "overview",
            ""
        ),

        "poster_path": poster,

        "tmdb_rating": details.get(
            "vote_average",
            ""
        )
    }



def add_tmdb_series_info(series):

    series = series.copy()

    series["style"] = ""
    series["country"] = ""
    series["overview"] = ""
    series["poster_path"] = ""
    series["tmdb_rating"] = None


    for index, row in series.iterrows():

        result = search_tmdb_series(
            row["title"]
        )


        if result:

            for col in [
                "style",
                "country",
                "overview",
                "poster_path",
                "tmdb_rating"
            ]:

                series.loc[index, col] = result.get(
                    col,
                    ""
                )


    return series

def search_series_tmdb(query):

    url = "https://api.themoviedb.org/3/search/tv"

    response = requests.get(
        url,
        params={
            "api_key": TMDB_API_KEY,
            "query": query,
            "language": "fr-FR"
        }
    )

    results = response.json().get("results", [])

    series = []

    for tv in results[:10]:

        series.append(
            {
                "id": tv["id"],
                "title": tv.get("name", ""),
                "year": (
                    tv.get("first_air_date", "")[:4]
                ),
                "overview": tv.get("overview", ""),
                "poster_path": (
                    "https://image.tmdb.org/t/p/w200"
                    + tv["poster_path"]
                )
                if tv.get("poster_path")
                else ""
            }
        )

    return series

def get_series_details_tmdb(series_id):

    response = requests.get(
        f"https://api.themoviedb.org/3/tv/{series_id}",
        params={
            "api_key": TMDB_API_KEY,
            "language": "fr-FR"
        }
    )

    details = response.json()

    genres = [
        GENRES_FR.get(
            g["name"],
            g["name"]
        )
        for g in details.get(
            "genres",
            []
        )
    ]

    countries = details.get(
        "origin_country",
        []
    )

    poster = ""

    if details.get("poster_path"):

        poster = (
            "https://image.tmdb.org/t/p/w500"
            + details["poster_path"]
        )
    
    external_ids = requests.get(
        f"https://api.themoviedb.org/3/tv/{series_id}/external_ids",
        params={
            "api_key": TMDB_API_KEY
        }
    ).json()

    tvdb_id = external_ids.get(
        "tvdb_id",
        ""
    )

    return {

    "tvdb_id": tvdb_id,

    "title": details.get(
        "name",
        ""
    ),

    "year": (
        details.get(
            "first_air_date",
            ""
        )[:4]
    ),

    "status": "continuing",

    "type": "series",

    "episodes": details.get(
        "number_of_episodes",
        0
    ),

    "progress": 0,

    "first_seen": "",

    "last_episode": "",

    "last_watch": "",

    "style": ", ".join(genres),

    "country": ", ".join(countries),

    "overview": details.get(
        "overview",
        ""
    ),

    "poster_path": poster,

    "tmdb_rating": details.get(
        "vote_average",
        ""
    )
}
