import streamlit as st

st.set_page_config(page_title="today")

st.title("Données du jour")


st.subheader("Moment du jour")

best_moment = st.text_input("Nom")


st.write(best_moment)