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

df_sport["Date"] = pd.to_datetime(df_sport["Date"])


# ==========================
# Filtre année
# ==========================

annees = sorted(
    df_sport["Date"].dt.year.unique(),
    reverse=True
)

annees_selection = st.selectbox(
    "Année",
    ["Toutes"] + annees
)


if annees_selection != "Toutes":

    df_filtre = df_sport[
        df_sport["Date"].dt.year == annees_selection
    ]

else:

    df_filtre = df_sport.copy()



# ==========================
# Données synthèse
# ==========================

activites = [
    "Danse",
    "Muscu",
    "Stretching",
    "Course",
    "Escalade",
    "Randonnée",
    "Autre",
]


totaux = df_filtre[activites].sum()

temps_total = totaux.sum()



# ==========================
# Première ligne dashboard
# ==========================

gauche, droite = st.columns(
    [1, 1.5]
)


# --------------------------
# KPIs
# --------------------------

with gauche:

    st.subheader("🏆 Synthèse")


    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Temps total",
            format_heures(temps_total)
        )

    with col2:
        st.metric(
            "Danse",
            format_heures(totaux["Danse"])
        )


    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "Course",
            format_heures(totaux["Course"])
        )

    with col4:
        st.metric(
            "Muscu",
            format_heures(totaux["Muscu"])
        )



# --------------------------
# Camembert
# --------------------------

with droite:

    st.subheader(
        "Répartition des activités"
    )


    df_repartition = (
        totaux
        .reset_index()
    )

    df_repartition.columns = [
        "Activite",
        "Temps"
    ]


    df_repartition = df_repartition[
        df_repartition["Temps"] > 0
    ]


    df_repartition["Affichage"] = (
        df_repartition["Temps"]
        .apply(format_heures)
    )


    fig = px.pie(
        df_repartition,
        names="Activite",
        values="Temps",
        hole=0.35,
    )


    fig.update_traces(
        hovertemplate=
        "%{label}<br>%{customdata}",
        customdata=df_repartition["Affichage"]
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# ==========================
# Evolution hebdomadaire
# ==========================

st.subheader(
    "📈 Temps de sport par semaine"
)


df_semaine = df_filtre.copy()


df_semaine["Total"] = (
    df_semaine[activites]
    .sum(axis=1)
)


# Cas : toutes les années
if annees_selection == "Toutes":

    df_semaine["Année"] = (
        df_semaine["Date"]
        .dt.year
    )

    df_semaine["Semaine"] = (
        df_semaine["Date"]
        .dt.isocalendar()
        .week
    )


    temps_semaine = (
        df_semaine
        .groupby(
            ["Année", "Semaine"]
        )["Total"]
        .sum()
        .reset_index()
    )


    temps_semaine["Heures"] = (
        temps_semaine["Total"] / 60
    )


    fig = px.line(
        temps_semaine,
        x="Semaine",
        y="Heures",
        color="Année",
        markers=True,
    )


    fig.update_layout(
        xaxis=dict(
            title="Semaine de l'année",
            dtick=4
        ),
        yaxis_title="Heures de sport",
        legend_title="Année"
    )


# Cas : une seule année
else:

    df_semaine["Semaine"] = (
        df_semaine["Date"]
        .dt.to_period("W")
        .apply(lambda x: x.start_time)
    )


    temps_semaine = (
        df_semaine
        .groupby("Semaine")["Total"]
        .sum()
        .reset_index()
    )


    temps_semaine["Heures"] = (
        temps_semaine["Total"] / 60
    )


    fig = px.line(
        temps_semaine,
        x="Semaine",
        y="Heures",
        markers=True,
    )


    fig.update_layout(
        xaxis_title="Semaine",
        yaxis_title="Heures de sport"
    )


st.plotly_chart(
    fig,
    use_container_width=True
)


# ==========================
# Tableau détaillé
# ==========================

st.subheader(
    "📅 Détail quotidien"
)


df_affichage = df_filtre.copy()


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