import streamlit as st
import pandas as pd

from scripts.importation_tvtime import tab_tv
from scripts.importation_myanimelist import tab_myanimelist

movies, series, series_episodes = tab_tv()
animes = tab_myanimelist()


st.title("🍿 Watchlist")


# =====================
# Dashboard
# =====================

# Nombre de films vus
nb_movies_watched = (
    movies["status"] == "watched"
).sum()

# Nombre de séries terminées
nb_series_finished = (
    series["status"] == "up_to_date"
).sum()

# Nombre de séries jamais terminées
nb_series_unfinished = (
    series["status"].isin(["continuing", "stopped"])
).sum()


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Films vus",
        nb_movies_watched
    )

with col2:
    st.metric(
        "Séries terminées",
        nb_series_finished
    )

with col3:
    st.metric(
        "Séries non terminées",
        nb_series_unfinished
    )


# =====================
# Films vus par mois
# =====================

movies_by_month = (
    movies[
        (movies["status"] == "watched")
        & (movies["watched_at"] >= "2023-01-01")
    ]
    .assign(month=lambda x: x["watched_at"].dt.to_period("M").astype(str))
    .groupby("month")
    .size()
)

st.subheader("Films vus par mois")

st.line_chart(movies_by_month)

# Nombre de films vus
nb_movies_watched = len(
    movies[movies["status"] == "watched"]
)

from scripts.gestion_watchlist import derniers_visionnages

watchlist = derniers_visionnages(movies, series)

st.header("Derniers visionnages")

st.dataframe(
    watchlist,
    use_container_width=True,
    hide_index=True
)


# =====================
# Tableaux de données
# =====================
st.header("Animes")

st.dataframe(
    animes,
    use_container_width=True,
    hide_index=True
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





st.header("Films")
st.dataframe(
    movies,
    use_container_width=True
)
