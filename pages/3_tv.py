import streamlit as st

from scripts.importation_tvtime import tab_tv

movies, series = tab_tv()

st.title("Données TV Time")

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