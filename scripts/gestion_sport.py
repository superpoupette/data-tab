import pandas as pd

from scripts.importation_2024 import prepare_2024

COLONNES_SPORT = [
    "Date",
    "Danse",
    "Muscu",
    "Stretching",
    "Course",
    "Escalade",
    "Randonnée",
    "Autre",
]


def creer_tableau_sport():
    return pd.DataFrame(columns=COLONNES_SPORT)


def importer_2024(df_sport, data2024):

    # Calcul du temps de danse
    danse = (
        data2024["Choree1_duree"].fillna(0)
        + data2024["Choree2_duree"].fillna(0)
        + data2024["Choree3_duree"].fillna(0)
        + data2024["Choree4_duree"].fillna(0)
        + data2024["Choree5_duree"].fillna(0)
    )

    # On ne conserve que les jours où il y a de la danse
    masque = danse > 0

    df_2024 = pd.DataFrame({
        "Date": data2024.loc[masque, "Date"],
        "Danse": danse.loc[masque],
        "Muscu": 0,
        "Stretching": 0,
        "Course": 0,
        "Escalade": 0,
        "Randonnée": 0,
        "Autre": 0,
    })

    # Ajout au tableau général
    df_sport = pd.concat([df_sport, df_2024], ignore_index=True)

    return df_sport


def charger_tableau_sport():
    """Construit le tableau complet de sport."""
    

    df_sport = creer_tableau_sport()

    data2024 = prepare_2024("data/2024.csv")   # à adapter
    df_sport = importer_2024(df_sport, data2024)

    return df_sport