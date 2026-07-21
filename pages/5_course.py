import pandas as pd
import streamlit as st

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
st.write(df[["Date de l'activité", "Distance"]].head(10))
st.write(df.dtypes)

km_semaine = (
    df
    .set_index("Date de l'activité")
    .resample("W")["Distance"]
    .sum()
)

st.subheader("📈 Kilomètres parcourus par semaine")

st.line_chart(
    km_semaine,
    use_container_width=True
)




st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)