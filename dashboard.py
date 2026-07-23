import streamlit as st
import pandas as pd
import plotly.express as px

from scripts.gestion_sport import charger_tableau_sport


def format_heures(minutes):
    return f"{round(minutes / 60)}h"



st.title("📊 Mon tableau de bord personnel")


# ==========================
# Chargement données
# ==========================

df_sport = charger_tableau_sport()


# Ajout année et semaine

df_sport["Annee"] = (
    df_sport["Date"]
    .dt.year
)

df_sport["Semaine"] = (
    df_sport["Date"]
    .dt.to_period("W")
    .astype(str)
)



# ==========================
# Filtre année
# ==========================

st.subheader("Analyse sportive")


annees = sorted(
    df_sport["Annee"]
    .unique()
)


choix_annee = st.selectbox(
    "Année",
    ["Toutes"] + annees
)


if choix_annee == "Toutes":

    df_filtre = df_sport.copy()

else:

    df_filtre = df_sport[
        df_sport["Annee"] == choix_annee
    ]



activites = [
    "Danse",
    "Muscu",
    "Stretching",
    "Course",
    "Escalade",
    "Randonnée",
    "Autre",
]



# ==========================
# Graphiques
# ==========================


col_gauche, col_droite = st.columns(
    [2,1]
)



# ---- Evolution semaine ----

with col_gauche:

    st.subheader(
        "Temps de sport par semaine"
    )


    df_semaine = (
        df_filtre
        .copy()
    )


    df_semaine["Total"] = (
        df_semaine[activites]
        .sum(axis=1)
    )


    evolution = (
        df_semaine
        .groupby("Semaine", as_index=False)
        ["Total"]
        .sum()
    )


    evolution["Heures"] = (
        evolution["Total"]
        /
        60
    )


    fig = px.line(
        evolution,
        x="Semaine",
        y="Heures",
        markers=True,
    )


    fig.update_layout(
        xaxis_title="Semaine",
        yaxis_title="Temps (heures)"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# ---- Répartition ----

with col_droite:

    st.subheader(
        "Répartition"
    )


    totaux = (
        df_filtre[activites]
        .sum()
        .reset_index()
    )


    totaux.columns = [
        "Activite",
        "Temps"
    ]


    totaux = totaux[
        totaux["Temps"] > 0
    ]


    totaux["Affichage"] = (
        totaux["Temps"]
        .apply(format_heures)
    )


    fig = px.pie(
        totaux,
        names="Activite",
        values="Temps",
        hole=0.35,
    )


    fig.update_traces(
        hovertemplate=
        "%{label}<br>%{customdata}",
        customdata=
        totaux["Affichage"]
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# ==========================
# Totaux année sélectionnée
# ==========================

st.subheader(
    "Total des activités"
)


totaux = (
    df_filtre[activites]
    .sum()
)


colonnes = st.columns(4)


for col, activite in zip(
    colonnes,
    activites[:4]
):

    col.metric(
        activite,
        format_heures(
            totaux[activite]
        )
    )


colonnes = st.columns(3)


for col, activite in zip(
    colonnes,
    activites[4:]
):

    col.metric(
        activite,
        format_heures(
            totaux[activite]
        )
    )



# ==========================
# Tableau détaillé
# ==========================

st.subheader(
    "📅 Détail quotidien"
)


df_affichage = df_sport.copy()


df_affichage["Total"] = (
    df_affichage[activites]
    .sum(axis=1)
)


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
    hide_index=True
)