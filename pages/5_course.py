import pandas as pd
import streamlit as st
import plotly.express as px

from scripts.importation_strava import charger_donnees_strava

st.set_page_config(
    page_title="Course",
    page_icon="🏃",
    layout="wide"
)

st.title("🏃 Dashboard Course")

# ==========================
# Chargement des données
# ==========================

df = charger_donnees_strava()
# Garder uniquement les courses à pied
df = df[
    df["Type d'activité"] == "Course à pied"
].copy()

# Conversion des dates
df["Date de l'activité"] = pd.to_datetime(
    df["Date de l'activité"],
    dayfirst=True
)

# ==========================
# Calcul des KPI
# ==========================

# Kilomètres parcourus
km_total = df["Distance"].sum()

# Vitesse moyenne
vitesse_moyenne = df["Vitesse moyenne"].mean()

# Distance maximale
distance_max = df["Distance"].max()

# Record sur 10 km
courses_10 = df[
    (df["Distance"] >= 9.9)
    & (df["Distance"] <= 10.1)
]

if len(courses_10):

    meilleur_temps = courses_10["Durée de déplacement"].min()

    heures = int(meilleur_temps // 3600)
    minutes = int((meilleur_temps % 3600) // 60)
    secondes = int(meilleur_temps % 60)

    if heures:
        meilleur_10 = f"{heures:d}:{minutes:02d}:{secondes:02d}"
    else:
        meilleur_10 = f"{minutes:d}:{secondes:02d}"

else:
    meilleur_10 = "-"

# ==========================
# Ligne de KPI
# ==========================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "🏃 Km totaux",
    f"{km_total:.1f} km"
)

c2.metric(
    "⚡ Vitesse moyenne",
    f"{vitesse_moyenne:.2f} km/h"
)

c3.metric(
    "🏅 Meilleur 10 km",
    meilleur_10
)

c4.metric(
    "📏 Sortie max",
    f"{distance_max:.1f} km"
)

st.divider()

# ==========================
# Km parcourus par semaine
# ==========================

df_graph = df.dropna(
    subset=[
        "Date de l'activité",
        "Distance"
    ]
).copy()

km_semaine = (
    df_graph
    .set_index("Date de l'activité")
    .resample("W")["Distance"]
    .sum()
    .reset_index()
)

st.subheader("Kilomètres parcourus par semaine")

fig = px.line(
    km_semaine,
    x="Date de l'activité",
    y="Distance",
    markers=True
)

fig.update_layout(
    xaxis_title="Semaine",
    yaxis_title="Kilomètres",
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# Tableau récapitulatif des sorties
# ==========================

st.subheader("Toutes les courses")


colonnes_affichees = [
    "Date de l'activité",
    "Nom de l'activité",
    "Description de l'activité",
    "Temps écoulé",
    "Distance",
    "Vitesse max.",
    "Vitesse moyenne"
]

df_resume = df[colonnes_affichees].copy()

# Tri du plus récent au plus ancien
df_resume = df_resume.sort_values(
    by="Date de l'activité",
    ascending=False
)

st.subheader("📋 Historique des sorties")

st.dataframe(
    df_resume,
    use_container_width=True,
    hide_index=True
)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)