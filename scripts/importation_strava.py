import pandas as pd




def charger_donnees_strava():

    df = pd.read_csv(
        "data/strava_activities.csv",
        encoding="latin1",
        low_memory=False
    )

    return df