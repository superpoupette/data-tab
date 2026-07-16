import pandas as pd


def reparer_texte(x):
    if isinstance(x, str):
        try:
            return x.encode("latin1").decode("utf-8")
        except:
            return x
    return x


df = df.applymap(reparer_texte)

def charger_donnees_strava():

    df = pd.read_csv(
        "data/strava_activities.csv",
        encoding="utf-8-sig"
    )

    df = df.applymap(reparer_texte)

    return df