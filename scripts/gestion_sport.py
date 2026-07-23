import pandas as pd

from scripts.importation_2024 import prepare_2024
from scripts.importation_2025 import prepare_2025

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
        + data2024["warmup"].fillna(0)
        + data2024["Autre"].fillna(0)
    )

    # Stretching : 10 minutes si la case est cochée
    stretching = data2024["Stretching"].fillna(False).astype(int) * 10

    # On ne conserve que les jours où il y a de la danse
    masque = (danse > 0) | (stretching > 0)

    df_2024 = pd.DataFrame({
        "Date": data2024.loc[masque, "Date"],
        "Danse": danse.loc[masque],
        "Muscu": 0,
        "Stretching": stretching.loc[masque],
        "Course": 0,
        "Escalade": 0,
        "Randonnée": 0,
        "Autre": 0,
    })

    # Ajout au tableau général
    df_sport = pd.concat([df_sport, df_2024], ignore_index=True)

    return df_sport

def importer_2025(df_sport, data2025):

    # Danse
    danse = data2025["Total Danse"].fillna(0)

    # Stretching
    stretch = data2025["Stretch"].fillna(False).astype(int) * 10
    stretch_split = data2025["Stretch_split"].fillna(False).astype(int) * 7
    stretch_bonus = data2025["Stretch_bonus"].fillna(0)

    stretching = stretch + stretch_split + stretch_bonus

    # On conserve uniquement les jours où il y a une activité
    masque = (danse > 0) | (stretching > 0)

    df_2025 = pd.DataFrame({
        "Date": data2025.loc[masque, "Date"],
        "Danse": danse.loc[masque],
        "Muscu": 0,
        "Stretching": stretching.loc[masque],
        "Course": 0,
        "Escalade": 0,
        "Randonnée": 0,
        "Autre": 0,
    })

    df_sport = pd.concat(
        [df_sport, df_2025],
        ignore_index=True
    )

    return df_sport



def charger_tableau_sport():
    """Construit le tableau complet de sport."""

    df_sport = creer_tableau_sport()

    # 2024
    data2024 = prepare_2024("data/2024.csv")
    df_sport = importer_2024(df_sport, data2024)

    # 2025
    data2025 = prepare_2025("data/2025.csv")
    df_sport = importer_2025(df_sport, data2025)

    # Tri chronologique
    df_sport = df_sport.sort_values("Date").reset_index(drop=True)

    return df_sport