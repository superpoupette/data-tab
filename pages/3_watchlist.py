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
