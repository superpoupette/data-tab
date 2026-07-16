import pandas as pd


def reparer_texte(texte):
    if not isinstance(texte, str):
        return texte

    marqueurs_corruption = ["Ã", "Â", "ð", "�"]

    if any(m in texte for m in marqueurs_corruption):
        try:
            return texte.encode("latin1").decode("utf-8")
        except Exception:
            return texte

    return texte

def charger_donnees_strava():
    df = pd.read_csv(
        "data/strava_activities.csv",
        encoding="latin1"
    )

    df = df.map(reparer_texte)

    return df