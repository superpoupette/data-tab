from datetime import date
import streamlit as st

from scripts.data_entry.dataframe import (
    create_today_dataframe,
    add_today_entry,
    save_dataframe_csv
)


st.set_page_config(page_title="Today")


st.title("Données du jour")


st.subheader("Général")

today = date.today().strftime('%d/%m/%Y')

st.write(f"📅 Aujourd'hui : {today}")


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



st.subheader("Danse")


col4, col5 = st.columns([3, 1])


with col4:

    Choree1_morceau = st.text_input(
        "Chorée morceau :",
        placeholder="Nom du morceau"
    )


with col5:

    Choree1_duree = st.text_input(
        "Durée :",
        placeholder="Minutes"
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
            sommeil_val,
            Choree1_morceau,
            Choree1_duree
        )


        save_to_google_sheet([
            today,
            best_moment,
            people_seen,
            int(people_work),
            sommeil_val,
            Choree1_morceau,
            Choree1_duree
        ])


        st.success("Donnée enregistrée !")


    except ValueError:

        st.error(
            "⚠️ Format incorrect pour le sommeil. Exemple attendu : 7 ou 7,5"
        )



st.subheader("Tableau des données")

st.dataframe(
    df,
    use_container_width=True
)