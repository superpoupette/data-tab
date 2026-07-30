import pandas as pd

from scripts.musique.google_sheet import (
    get_music_sheet
)

from scripts.musique.spotify_api import (
    enrichir_album
)



COLONNES_SPOTIFY = [
    "spotify_id",
    "spotify_date_sortie",
    "nb_titres",
    "cover_url",
    "spotify_artiste",
    "spotify_album",
    "spotify_genres"
]


def enrichir_google_sheet():

    sheet = get_music_sheet()

    data = sheet.get_all_records()

    df = pd.DataFrame(data)


    for colonne in COLONNES_SPOTIFY:

        if colonne not in df.columns:
            df[colonne] = ""

    for colonne in COLONNES_SPOTIFY:
        df[colonne] = df[colonne].astype(str)


    for index, ligne in df.iterrows():

        # déjà enrichi
        if ligne["spotify_id"]:
            continue


        infos = enrichir_album(
            ligne["spotify_id"]
        )


        if infos:

            for cle, valeur in infos.items():

                if valeur is None:
                    valeur = ""

                df.loc[index, cle] = str(valeur)



    sheet.clear()

    sheet.update(
        [
            df.columns.tolist()
        ]
        +
        df.values.tolist()
    )