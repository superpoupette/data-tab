import streamlit as st
import pandas as pd

from scripts.importation_tvtime import tab_tv

movies, series, series_episodes = tab_tv()


st.title("🍿 Watchlist")

# =====================
# Dashboard
# =====================


# Nombre de films vus
nb_movies_watched = len(
    movies[movies["status"] == "watched"]
)


# =====================
# Films et séries visionnés
# =====================

watched_movies = movies[
    movies["status"] == "watched"
].copy()

watched_movies = watched_movies.rename(
    columns={"watched_at": "last_watch"}
)


watched_series = series[
    series["status"] == "up_to_date"
].copy()


watched_movies = watched_movies[
    [
        "title",
        "year",
        "type",
        "last_watch"
    ]
]

watched_series = watched_series[
    [
        "title",
        "year",
        "type",
        "last_watch"
    ]
]


watched = pd.concat(
    [watched_movies, watched_series],
    ignore_index=True
)


watched = watched.sort_values(
    by="last_watch",
    ascending=False
)


st.header("🎬 Films et Séries visionnés")

st.dataframe(
    watched,
    use_container_width=True,
    hide_index=True
)


# =====================
# Tableaux de données
# =====================

st.header("Films")
st.dataframe(
    movies,
    use_container_width=True
)

st.header("Séries")
st.dataframe(
    series,
    use_container_width=True
)

st.header("Épisodes de séries")
st.dataframe(
    series_episodes,
    use_container_width=True
)

from scripts.importation_anilist import load_anilist

anime = load_anilist("Poupette")

st.dataframe(anime)
