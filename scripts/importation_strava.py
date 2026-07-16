import pandas as pd


def reparer_texte(texte):
    if isinstance(texte, str):
        try:
            return texte.encode("latin1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return texte
    return texte


def charger_donnees_strava():
    df = pd.read_csv(
        "data/strava_activities.csv",
        encoding="latin1"
    )

    df = df.map(reparer_texte)

    return df