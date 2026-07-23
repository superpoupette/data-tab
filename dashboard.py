import streamlit as st
import pandas as pd
import plotly.express as px

from scripts.gestion_sport import charger_tableau_sport


st.title("📊 Mon tableau de bord personnel")


# Chargement des données
df_sport = charger_tableau_sport()


# ==========================
# Synthèse des activités
# ==========================


activites = [
    "Danse",
    "Muscu",
    "Stretching",
    "Course",
    "Escalade",
    "Randonnée",
]

totaux = df_sport[activites].sum()


# Affichage en colonnes
colonnes = st.columns(len(activites))

for col, activite in zip(colonnes, activites):
    col.metric(
        label=activite,
        value=f"{totaux[activite]:.0f} min"
    )


# ==========================
# Graphique répartition
# ==========================


df_repartition = (
    totaux
    .reset_index()
)

df_repartition.columns = [
    "Activite",
    "Temps"
]


# Suppression des activités à 0
df_repartition = df_repartition[
    df_repartition["Temps"] > 0
]


fig = px.pie(
    df_repartition,
    names="Activite",
    values="Temps",
    hole=0.3,
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ==========================
# Tableau détaillé
# ==========================

st.subheader("📅 Détail quotidien")

st.dataframe(
    df_sport,
    use_container_width=True,
    hide_index=True,
)