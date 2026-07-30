import pandas as pd
import streamlit as st

from scripts.musique.google_sheet import get_music_sheet
from scripts.musique.spotify_api import enrichir_album


COLONNES_SPOTIFY = [
    "spotify_url",
    "cover_url",
    "spotify_date_sortie",
    "nb_titres",
    "spotify_artiste",
    "spotify_album",
    "spotify_genres"
]


def enrichir_google_sheet():

    sheet = get_music_sheet()

    data = sheet.get_all_records()

    df = pd.DataFrame(data)

    st.write("Nombre de lignes :", len(df))

    # création des colonnes manquantes
    for colonne in COLONNES_SPOTIFY:
        if colonne not in df.columns:
            df[colonne] = ""


    for index, ligne in df.iterrows():

        spotify_id = str(ligne["spotify_id"]).strip()

        st.write(
            "Traitement :",
            ligne["Album"],
            spotify_id
        )


        if spotify_id == "" or spotify_id == "0":
            continue


        infos = enrichir_album(
            spotify_id
        )


        st.write(
            "Retour Spotify :",
            infos
        )


        if infos:

            for cle, valeur in infos.items():

                if cle in df.columns:
                    df.loc[index, cle] = valeur


    st.write(df.head())


    sheet.clear()

    sheet.update(
        [
            df.columns.tolist()
        ]
        +
        df.values.tolist()
    )

    st.success("Enrichissement terminé")