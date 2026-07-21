import pandas as pd
import streamlit as st
import plotly.express as px

from scripts.importation_strava import charger_donnees_strava


st.set_page_config(
    page_title="Course",
    page_icon="🏃",
    layout="wide"
)


# ==========================
# Fonctions utilitaires
# ==========================

def separateur():
    st.markdown(
        """
        <hr style="
            border: none;
            border-top: 1px solid #d9d9d9;
            margin: 25px 0;
        ">
        """,
        unsafe_allow_html=True
    )


def format_temps(secondes):
    if pd.isna(secondes):
        return ""

    secondes = int(secondes)

    heures = secondes // 3600
    minutes = (secondes % 3600) // 60
    secondes = secondes % 60

    return f"{heures:02d}:{minutes:02d}:{secondes:02d}"


def vitesse_kmh(vitesse):
    if pd.isna(vitesse):
        return ""

    return f"{vitesse * 3.6:.1f} km/h"


def vitesse_vers_allure(vitesse_ms):
    if pd.isna(vitesse_ms) or vitesse_ms <= 0:
        return ""

    secondes_par_km = 1000 / vitesse_ms

    minutes = int(secondes_par_km // 60)
    secondes = int(secondes_par_km % 60)

    return f"{minutes}:{secondes:02d}/km"


# ==========================
# Titre
# ==========================

st.title("🏃 Dashboard Course")


# ==========================
# Chargement des données
# ==========================

df = charger_donnees_strava()


df = df[
    df["Type d'activité"] == "Course à pied"
].copy()


# ==========================
# Données utilisées pour calculs
# ==========================

df_calculs = df[
    df["Nom de l'activité"] != "Bah super le bug 😬🤖"
].copy()


# ==========================
# KPI
# ==========================

km_total = df_calculs["Distance"].sum()


vitesse_moyenne = (
    df_calculs["Vitesse moyenne"]
    .dropna()
    .mean()
)


if vitesse_moyenne > 0:

    secondes_par_km = 1000 / vitesse_moyenne

    minutes_allure = int(secondes_par_km // 60)
    secondes_allure = int(secondes_par_km % 60)

    allure_moyenne = (
        f"{minutes_allure}:{secondes_allure:02d}/km"
    )

else:
    allure_moyenne = "-"


distance_max = df_calculs["Distance"].max()


courses_10 = df_calculs[
    (df_calculs["Distance"] >= 9.9)
    &
    (df_calculs["Distance"] <= 10.1)
]


if len(courses_10):

    meilleur_temps = (
        courses_10["Durée de déplacement"]
        .min()
    )

    heures = int(meilleur_temps // 3600)
    minutes = int((meilleur_temps % 3600) // 60)
    secondes = int(meilleur_temps % 60)


    if heures:
        meilleur_10 = (
            f"{heures}:{minutes:02d}:{secondes:02d}"
        )
    else:
        meilleur_10 = (
            f"{minutes}:{secondes:02d}"
        )

else:
    meilleur_10 = "-"


# ==========================
# Affichage KPI
# ==========================

c1, c2, c3, c4 = st.columns(4)


c1.metric(
    "🏃 Km totaux",
    f"{km_total:.1f} km"
)

c2.metric(
    "🏃 Allure moyenne",
    allure_moyenne
)

c3.metric(
    "🏅 Meilleur 10 km",
    meilleur_10
)

c4.metric(
    "📏 Sortie max",
    f"{distance_max:.1f} km"
)


separateur()