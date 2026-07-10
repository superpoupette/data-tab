from datetime import date
import streamlit as st

from scripts.data_entry.dataframe import (
    create_today_dataframe,
    add_today_entry,
    save_to_google_sheet
)

from scripts.danse.google_sheet import add_danse_google_sheet

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



from scripts.danse.google_sheet import (
    load_danse_google_sheet,
    add_practice_time
)


st.subheader("Danse")

danses = load_danse_google_sheet()

danses_en_cours = danses[
    danses["statut"] == "en cours"
]

if len(danses_en_cours) > 0:

    danses_labels = (
        danses_en_cours["artiste"]
        + " - "
        + danses_en_cours["titre"]
    )

    col1, col2, col3 = st.columns([4, 1, 1])

    with col1:
        choix_danse = st.selectbox(
            "Chorégraphie travaillée :",
            danses_labels
        )

    with col2:
        duree_danse = st.number_input(
            "Durée (min)",
            min_value=0,
            step=5
        )

    with col3:
        st.write("")   # espace pour aligner
        st.write("")

        ajouter = st.button(
            "💃 Ajouter",
            use_container_width=True
        )

    if ajouter:

        ligne = danses_en_cours[
            (
                danses_en_cours["artiste"]
                + " - "
                + danses_en_cours["titre"]
            ) == choix_danse
        ].iloc[0]

        succes = add_practice_time(
            ligne["artiste"],
            ligne["titre"],
            duree_danse
        )

        if succes:
            st.success(
                "Temps ajouté à la chorégraphie !"
            )
        else:
            st.error(
                "Impossible de trouver la chorégraphie."
            )

else:
    st.info(
        "Aucune chorégraphie en cours."
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


#Nouvelle chorégraphie
st.subheader("Nouvelle chorégraphie")

col6, col7, col8, col9 = st.columns([3, 3, 3, 1])

with col6:
    new_artiste=st.text_input(
        "Artiste :",
    )

with col7:
    new_titre=st.text_input(
        "Titre :",
    )

with col8:
    new_choregraphe=st.text_input(
        "Choregraphe :",
    )

with col9:
    new_duree=st.text_input(
        "Durée :",
        placeholder="min",
        key="new_choreo_duree"
    )

if st.button("➕ Ajouter la chorégraphie"):

    if (
        new_artiste.strip()
        and new_titre.strip()
    ):

        add_danse_google_sheet(
            new_artiste,
            new_titre,
            new_choregraphe,
            new_duree
        )

        st.success(
            "Nouvelle chorégraphie ajoutée !"
        )

    else:

        st.error(
            "L'artiste et le titre sont obligatoires."
        )

st.subheader("Tableau des données")

st.dataframe(
    df,
    use_container_width=True
)