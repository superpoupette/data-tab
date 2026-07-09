import streamlit as st

st.set_page_config(page_title="today")

st.title("Données du jour")


st.subheader("Moment du jour")

texte = st.text_area(
    "Notes du jour",
    placeholder="Écris ici...",
    height=200
)