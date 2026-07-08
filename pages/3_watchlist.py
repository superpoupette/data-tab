mport streamlit as st
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

# Nombre de séries terminées
nb_series_finished = len(
    series[series["status"] == "up_to_date"]
)


col1, col2 = st.columns(2)

with col1:
    st.metric(
        "🎬 Films vus",
        nb_movies_watched
    )

with col2:
    st.metric(
        "📺 Séries terminées",
        nb_series_finished
    )

# Films vus par année
movies_by_year = (
    movies[movies["status"] == "watched"]
    .assign(year=lambda x: x["watched_at"].dt.year)
    .groupby("year")
    .size()
)


# Séries terminées par année
series_by_year = (
    series[series["status"] == "up_to_date"]
    .assign(year=lambda x: x["watched_at"].dt.year)
    .groupby("year")
    .size()
)


col1, col2 = st.columns(2)

with col1:
    st.subheader("Films vus par année")
    st.bar_chart(movies_by_year)

with col2:
    st.subheader("Séries terminées par année")
    st.bar_chart(series_by_year)

# =====================
# Films et séries visionnés
# =====================

watched_movies = movies[
    movies["status"] == "watched"
]

watched_series = series[
    series["status"] == "up_to_date"
]


watched = pd.concat(
    [watched_movies, watched_series],
    ignore_index=True
)


watched = watched[
    [
        "title",
        "year",
        "type",
        "watched_at"
    ]
]


watched = watched.sort_values(
    by="watched_at",
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
