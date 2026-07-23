import streamlit as st
import pandas as pd
import plotly.express as px

from scripts.gestion_sport import charger_tableau_sport


def format_heures(minutes):
    """Convertit des minutes en affichage heures arrondies."""
    return f"{round(minutes / 60)}h"


st.title("📊 Mon tableau de bord personnel")


# Chargement des données
df_sport = charger_tableau_sport()


# ==========================
# Synthèse des activités
# ==========================

st.subheader("🏆 Total des activités")


activites = [
    "Danse",
    "Muscu",
    "Stretching",
    "Course",
    "Escalade",
    "Randonnée",
    "Autre",
]


totaux = df_sport[activites].sum()


# Première ligne
colonnes = st.columns(4)

for col, activite in zip(colonnes, activites[:4]):
    col.metric(
        label=activite,
        value=format_heures(totaux[activite])
    )


# Deuxième ligne
colonnes = st.columns(3)

for col, activite in zip(colonnes, activites[4:]):
    col.metric(
        label=activite,
        value=format_heures(totaux[activite])
    )


# ==========================
# Graphique répartition
# ==========================

st.subheader("📈 Répartition du temps par sport")


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


# Texte affiché en heures
df_repartition["Temps_affichage"] = (
    df_repartition["Temps"]
    .apply(format_heures)
)


fig = px.pie(
    df_repartition,
    names="Activite",
    values="Temps",
    hole=0.3,
)


fig.update_traces(
    hovertemplate="%{label}<br>%{customdata}",
    customdata=df_repartition["Temps_affichage"]
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ==========================
# Tableau détaillé
# ==========================

st.subheader("📅 Détail quotidien")


df_affichage = df_sport.copy()


# Ajout du total pour l'affichage uniquement
df_affichage["Total"] = (
    df_affichage[activites]
    .sum(axis=1)
)


# Mise en heures pour l'affichage
for col in ["Total"] + activites:
    df_affichage[col] = (
        df_affichage[col]
        .apply(format_heures)
    )


# Remettre Total juste après Date
colonnes = [
    "Date",
    "Total",
    "Danse",
    "Muscu",
    "Stretching",
    "Course",
    "Escalade",
    "Randonnée",
    "Autre",
]

df_affichage = df_affichage[colonnes]


st.dataframe(
    df_affichage,
    use_container_width=True,
    hide_index=True,
)