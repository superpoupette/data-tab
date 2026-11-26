from datetime import date
import streamlit as st

from scripts.data_entry.dataframe import (
    create_today_dataframe,
    add_today_entry,
    save_to_google_sheet
)

from scripts.danse.google_sheet import (
    add_danse_google_sheet,
    load_danse_google_sheet,
    add_practice_time
)

st.set_page_config(
    page_title="Today",
    page_icon="☀️",
    layout="wide"
)


st.title("Données du jour")

st.subheader("Général")

# Date sélectionnable (aujourd'hui par défaut)
selected_date = st.date_input(
    "📅 Date",
    value=date.today(),
    format="DD/MM/YYYY"
)

today = selected_date.strftime("%d/%m/%Y")

best_moment = st.text_input(
    "Meilleur moment du jour :"
)

col1, col2, col3 = st.columns([1, 3, 3])

with col1:
    st.write("Travail :")

    people_work = st.checkbox(
        " ",
        label_visibility="collapsed"
    )

with col2:
    people_seen = st.text_input(
        "Personnes vues aujourd'hui :",
        placeholder="Ex : Alice, Marc, Julie"
    )

with col3:
    sommeil = st.text_input(
        "Sommeil (heures) :",
        placeholder="Ex : 7,5"
    )

# Chargement du dataframe existant
df = create_today_dataframe()

if st.button("💾 Sauvegarder"):

    try:

        if sommeil.strip() == "":
            sommeil_val = None
        else:
            sommeil_val = float(
                sommeil.replace(",", ".")
            )

        df = add_today_entry(
            df,
            today,
            best_moment,
            people_seen,
            int(people_work),
            sommeil_val
        )

        save_to_google_sheet([
            today,
            best_moment,
            people_seen,
            int(people_work),
            sommeil_val
        ])

        st.success(
            f"Donnée enregistrée pour le {today} !"
        )

    except ValueError:

        st.error(
            "⚠️ Format incorrect pour le sommeil. Exemple attendu : 7 ou 7,5"
        )



