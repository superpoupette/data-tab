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


st.subheader("Nouvelle chorégraphie")

# Ligne 1
col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    new_artiste = st.text_input(
        "Artiste",
        key="new_artiste"
    )

with col2:
    new_titre = st.text_input(
        "Titre",
        key="new_titre"
    )

with col3:
    new_choregraphe = st.text_input(
        "Chorégraphe",
        key="new_choregraphe"
    )

# Ligne 2
col4, col5 = st.columns([2, 1])

with col4:
    new_style = st.selectbox(
        "Style",
        [
            "Urban",
            "Kpop girl",
            "Kpop boy",
            "Jazz",
            "Lyrical",
            "Street Jazz",
            "Dancehall",
            "Waacking/voguing",
            "Heels"
        ],
        key="new_style"
    )

with col5:
    new_duree = st.number_input(
        "Durée (s)",
        min_value=0,
        step=10,
        key="new_duree"
    )

# Ligne 3
if st.button(
    "➕ Ajouter la chorégraphie",
    use_container_width=True
):
    add_danse_google_sheet(
        artiste=new_artiste,
        titre=new_titre,
        choregraphe=new_choregraphe,
        style=new_style,
        duree=new_duree
    )

    st.success("Chorégraphie ajoutée !")


st.subheader("Tableau des données")

st.dataframe(
    df,
    use_container_width=True
)