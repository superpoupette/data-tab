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

# Allure moyenne globale
vitesse_moyenne = df["Vitesse moyenne"].mean()

secondes_par_km = 1000 / vitesse_moyenne

minutes_allure = int(secondes_par_km // 60)
secondes_allure = int(secondes_par_km % 60)

allure_moyenne = f"{minutes_allure}:{secondes_allure:02d}/km"

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

st.divider()

# ==========================
# Graphiques performances
# ==========================

col1, col2 = st.columns(2)


# ==========================
# Km parcourus par semaine
# ==========================

with col1:

    st.subheader("📈 Km par semaine")


    annees = sorted(
        df["Date de l'activité"].dt.year.unique(),
        reverse=True
    )

    annee_km = st.selectbox(
        "Année",
        annees,
        key="annee_km"
    )


    df_annee = df[
        df["Date de l'activité"].dt.year == annee_km
    ].copy()


    km_semaine = (
        df_annee
        .set_index("Date de l'activité")
        .resample("W")["Distance"]
        .sum()
        .reset_index()
    )


    fig_km = px.line(
        km_semaine,
        x="Date de l'activité",
        y="Distance",
        markers=True
    )


    fig_km.update_layout(
        xaxis_title="Semaine",
        yaxis_title="Km",
        height=350
    )


    st.plotly_chart(
        fig_km,
        use_container_width=True
    )



# ==========================
# Allure par sortie
# ==========================

with col2:

    st.subheader("🏃 Allure par sortie")


    annee_allure = st.selectbox(
        "Année",
        annees,
        key="annee_allure"
    )


    df_allure = df[
        df["Date de l'activité"].dt.year == annee_allure
    ].copy()


    # Calcul allure min/km
    df_allure["Allure"] = (
        1000 / df_allure["Vitesse moyenne"]
    ) / 60


    fig_allure = px.line(
        df_allure.sort_values("Date de l'activité"),
        x="Date de l'activité",
        y="Allure",
        markers=True
    )


    fig_allure.update_layout(
        xaxis_title="Date",
        yaxis_title="Allure (min/km)",
        height=350,
        yaxis=dict(
            autorange="reversed"
        )
    )


    st.plotly_chart(
        fig_allure,
        use_container_width=True
    )

# ==========================
# Tableau récapitulatif des sorties
# ==========================

st.subheader("📋 Historique des sorties")


# --------------------------
# Fonctions de formatage
# --------------------------

def format_temps(secondes):
    """Convertit des secondes en HH:MM:SS"""
    if pd.isna(secondes):
        return ""

    secondes = int(secondes)

    heures = secondes // 3600
    minutes = (secondes % 3600) // 60
    secondes = secondes % 60

    return f"{heures:02d}:{minutes:02d}:{secondes:02d}"


def vitesse_kmh(vitesse):
    """Convertit m/s en km/h"""
    if pd.isna(vitesse):
        return ""

    return f"{vitesse * 3.6:.1f} km/h"


def vitesse_vers_allure(vitesse_ms):
    """Convertit m/s en allure min/km"""
    if pd.isna(vitesse_ms) or vitesse_ms <= 0:
        return ""

    secondes_par_km = 1000 / vitesse_ms

    minutes = int(secondes_par_km // 60)
    secondes = int(secondes_par_km % 60)

    return f"{minutes}:{secondes:02d}/km"


# --------------------------
# Colonnes affichées
# --------------------------

colonnes_affichees = [
    "Date de l'activité",
    "Nom de l'activité",
    "Description de l'activité",
    "Temps écoulé",
    "Distance",
    "Vitesse max.",
    "Vitesse moyenne"
]


# Création du tableau résumé
df_resume = df[colonnes_affichees].copy()


# --------------------------
# Mise en forme des données
# --------------------------

# Temps
df_resume["Temps écoulé"] = (
    df_resume["Temps écoulé"]
    .apply(format_temps)
)


# Distance
df_resume["Distance"] = (
    df_resume["Distance"]
    .apply(lambda x: f"{x:.2f} km" if pd.notna(x) else "")
)


# Ajout de l'allure moyenne avant la vitesse moyenne
df_resume.insert(
    df_resume.columns.get_loc("Vitesse moyenne"),
    "Allure moyenne",
    df["Vitesse moyenne"].apply(vitesse_vers_allure)
)


# Vitesses
df_resume["Vitesse max."] = (
    df_resume["Vitesse max."]
    .apply(vitesse_kmh)
)

df_resume["Vitesse moyenne"] = (
    df_resume["Vitesse moyenne"]
    .apply(vitesse_kmh)
)


# --------------------------
# Tri du plus récent au plus ancien
# --------------------------

df_resume = df_resume.sort_values(
    by="Date de l'activité",
    ascending=False
)


# --------------------------
# Affichage
# --------------------------

st.dataframe(
    df_resume,
    use_container_width=True,
    hide_index=True
)