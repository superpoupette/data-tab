import streamlit as st

st.set_page_config(page_title="today")

st.title("Données du jour")


st.subheader("Mood")

best_moment = st.text_input("Meilleur moment du jour :")


st.write(best_moment)