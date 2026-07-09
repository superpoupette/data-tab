from datetime import date
import streamlit as st

from scripts.data_entry.dataframe import (
    create_today_dataframe,
    add_today_entry
)

st.set_page_config(page_title="Today")

st.title("Données du jour")

today = date.today().strftime('%d/%m/%Y')

st.write(f"📅 Aujourd'hui : {today}")

st.subheader("Mood")

best_moment = st.text_input("Meilleur moment du jour :")


# Ligne personnes vues + travail
col1, col2 = st.columns([1, 5])

with col1:
    people_work = st.checkbox("💼")

with col2:
    people_seen = st.text_input(
        "Personnes vues aujourd'hui :",
        placeholder="Ex : Alice, Marc, Julie"
    )


# Création du dataframe
df = create_today_dataframe()


if st.button("💾 Sauvegarder"):

    df = add_today_entry(
        df,
        today,
        best_moment,
        people_seen,
        int(people_work)
    )


st.subheader("Tableau des données")

st.dataframe(df, use_container_width=True)