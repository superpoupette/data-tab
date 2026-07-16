import pandas as pd


def charger_donnees_strava():
    """
    Charge le fichier CSV Strava et retourne un DataFrame.
    """

    df = pd.read_csv(
        "data/strava_activities.csv",
        encoding="latin1"
    )

    return df