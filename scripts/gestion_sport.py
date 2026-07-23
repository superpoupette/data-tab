import pandas as pd

from scripts.importation_2024 import prepare_2024
from scripts.importation_2025 import prepare_2025
from scripts.importation_strava import charger_donnees_strava
from scripts.importation_2026 import clean_danses_2026


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

    # Musculation
    muscu = data2025["Muscu_duree"].fillna(0)

    # Escalade
    escalade = data2025["Escalade"].fillna(0)

    # On conserve uniquement les jours avec une activité
    masque = (
        (danse > 0)
        | (stretching > 0)
        | (muscu > 0)
        | (escalade > 0)
    )

    df_2025 = pd.DataFrame({
        "Date": data2025.loc[masque, "Date"],
        "Danse": danse.loc[masque],
        "Muscu": muscu.loc[masque],
        "Stretching": stretching.loc[masque],
        "Course": 0,
        "Escalade": escalade.loc[masque],
        "Randonnée": 0,
        "Autre": 0,
    })

    df_sport = pd.concat(
        [df_sport, df_2025],
        ignore_index=True
    )

    return df_sport

def importer_strava(df_sport, data_strava):

    # Initialisation des colonnes en float
    course = pd.Series(0.0, index=data_strava.index)
    randonnee = pd.Series(0.0, index=data_strava.index)

    # Conversion du temps écoulé en minutes
    temps = data_strava["Temps écoulé"].fillna(0) / 60

    # Répartition selon le type d'activité
    masque_course = (
        data_strava["Type d'activité"] == "Course à pied"
    )

    masque_rando = (
        data_strava["Type d'activité"] == "Randonnée"
    )

    course.loc[masque_course] = temps.loc[masque_course]

    randonnee.loc[masque_rando] = temps.loc[masque_rando]

    # On conserve uniquement les activités utiles
    masque = (course > 0) | (randonnee > 0)

    df_strava = pd.DataFrame({
        "Date": data_strava.loc[masque, "Date de l'activité"].dt.normalize(),
        "Danse": 0,
        "Muscu": 0,
        "Stretching": 0,
        "Course": course.loc[masque],
        "Escalade": 0,
        "Randonnée": randonnee.loc[masque],
        "Autre": 0,
    })

    df_sport = pd.concat(
        [df_sport, df_strava],
        ignore_index=True
    )

    return df_sport

def importer_2026(df_sport, data2026):

    # Danse
    danse = data2026["Danse"].fillna(0)

    # Stretching
    stretching = data2026["Stretch"].fillna(0)

    # On garde uniquement les lignes avec une activité
    masque = (
        (danse > 0)
        | (stretching > 0)
    )

    df_2026 = pd.DataFrame({
        "Date": data2026.loc[masque, "Date"],
        "Danse": danse.loc[masque],
        "Muscu": 0,
        "Stretching": stretching.loc[masque],
        "Course": 0,
        "Escalade": 0,
        "Randonnée": 0,
        "Autre": 0,
    })

    df_sport = pd.concat(
        [df_sport, df_2026],
        ignore_index=True
    )

    return df_sport

def charger_tableau_sport():

    df_sport = creer_tableau_sport()

    # 2024
    data2024 = prepare_2024("data/2024.csv")
    df_sport = importer_2024(df_sport, data2024)

    # 2025
    data2025 = prepare_2025("data/2025.csv")
    df_sport = importer_2025(df_sport, data2025)

    # 2026
    data2026 = clean_danses_2026()
    df_sport = importer_2026(df_sport, data2026)

    # Strava
    data_strava = charger_donnees_strava()
    df_sport = importer_strava(df_sport, data_strava)

    # Tri par date
    df_sport = (
        df_sport
        .sort_values("Date")
        .reset_index(drop=True)
    )

    return df_sport