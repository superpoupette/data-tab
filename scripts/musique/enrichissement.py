import pandas as pd

from scripts.musique.google_sheet import (
    get_music_sheet
)

from scripts.musique.spotify_api import (
    enrichir_album
)



COLONNES_SPOTIFY = [
    "spotify_id",
    "spotify_url",
    "cover_url",
    "spotify_date_sortie",
    "nb_titres",
    "popularite",
    "spotify_artiste"
]


def enrichir_google_sheet():

    sheet = get_music_sheet()

    data = sheet.get_all_records()

    df = pd.DataFrame(data)


    for colonne in COLONNES_SPOTIFY:

        if colonne not in df.columns:
            df[colonne] = ""


    for index, ligne in df.head(5).iterrows():

        # déjà enrichi
        if ligne["spotify_id"]:
            continue


        infos = enrichir_album(
            ligne["Album"],
            ligne["Artiste"]
        )


        if infos:

            for cle, valeur in infos.items():

                df.loc[index, cle] = valeur



    sheet.clear()

    sheet.update(
        [
            df.columns.tolist()
        ]
        +
        df.values.tolist()
    )