from datetime import date
import streamlit as st

from scripts.data_entry.dataframe import create_today_dataframe

st.set_page_config(page_title="Today")

st.title("Données du jour")
st.write(f"📅 Aujourd'hui : {date.today().strftime('%d/%m/%Y')}")

st.subheader("Mood")

best_moment = st.text_input("Meilleur moment du jour :")

st.write(best_moment)


st.button("💾 Sauvegarder")

# Création du tableau
df = create_today_dataframe()

st.subheader("Tableau des données")

st.dataframe(df, use_container_width=True)