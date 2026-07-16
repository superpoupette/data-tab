import pandas as pd


def reparer_texte(x):
    if isinstance(x, str):
        try:
            return x.encode("latin1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return x
    return x


def charger_donnees_strava():

    df = pd.read_csv(
        "data/strava_activities.csv",
        encoding="latin1"
    )

    # Réparation du texte corrompu
    df = df.applymap(reparer_texte)

    return df