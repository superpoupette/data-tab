import pandas as pd


def reparer_texte(texte):
    if isinstance(texte, str):
        try:
            return texte.encode("latin1").decode("utf-8")
        except Exception:
            return texte
    return texte


def charger_donnees_strava():

    df = pd.read_csv(
        "data/strava_activities.csv",
        encoding="latin1",
        low_memory=False
    )

    # Correction de tous les champs texte
    for colonne in df.select_dtypes(include="object").columns:
        df[colonne] = df[colonne].apply(reparer_texte)

    return df