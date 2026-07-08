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

from scripts.gestion_watchlist import derniers_visionnages

watchlist = derniers_visionnages(movies, series)

st.header("🎬 Films et Séries visionnés")

st.dataframe(
    watchlist,
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

st.header("Animés")

from scripts.importation_anilist import load_anilist

anime = load_anilist("Poupette")

st.dataframe(anime)
