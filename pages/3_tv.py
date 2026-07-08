import streamlit as st

from scripts.importation_tvtime import tab_tv

movies, series, series_episodes = tab_tv()

st.title("🍿 Watchlist")

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
