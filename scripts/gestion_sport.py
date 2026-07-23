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
    df_sport["Date"] = data2024["Date"]
    df_sport["Danse"] = data2024["Total Danse"]

    for col in COLONNES_SPORT:
        if col not in ("Date", "Danse"):
            df_sport[col] = 0

    return df_sport


def charger_tableau_sport():
    """Construit le tableau complet de sport."""

    df_sport = creer_tableau_sport()

    data2024 = prepare_2024("data/2024.csv")   # à adapter
    df_sport = importer_2024(df_sport, data2024)

    return df_sport