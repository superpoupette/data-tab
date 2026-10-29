import streamlit as st
import pandas as pd
import plotly.express as px

from scripts.gestion_sport import charger_tableau_sport
from scripts.objectifs import (
    pompes_2026,
    pages_dessin,
    ajouter_page_dessin,
    retirer_page_dessin,
    detox,
    ajouter_detox,
    retirer_detox
)

def format_heures(minutes):
    return f"{round(minutes / 60)}h"


def separateur():
    st.markdown(
        """
        <hr style="
            border: none;
            border-top: 1px solid #d9d9d9;
            margin: 20px 0;
        ">
        """,
        unsafe_allow_html=True
    )


st.title("Tableau de bord")

# ==========================
# Chargement données
# ==========================

df_sport = charger_tableau_sport()

df_sport["Date"] = pd.to_datetime(
    df_sport["Date"]
)

nb_pompes = pompes_2026()
nb_pages = pages_dessin()
nb_detox = detox()

# ==========================
# Filtre année
# ==========================
st.header("Sport")

annees = sorted(
    df_sport["Date"]
    .dt.year
    .dropna()
    .unique(),
    reverse=True
)


annees_selection = st.selectbox(
    "Année",
    ["Toutes"] + list(annees)
)


if annees_selection == "Toutes":

    df_filtre = df_sport.copy()

else:

    df_filtre = df_sport[
        df_sport["Date"].dt.year == annees_selection
    ]



# ==========================
# Activités
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


totaux = (
    df_filtre[activites]
    .sum()
)


temps_total = totaux.sum()



# ==========================
# Première ligne dashboard
# ==========================



gauche, droite = st.columns(
    [1, 1.5]
)



# ==========================
# KPI
# ==========================

with gauche:

    st.subheader("Synthèse")


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



# ==========================
# Camembert
# ==========================

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

    # Couleurs fixes
    couleurs_activites = {
        "Course": "#F6C667",      # Jaune doux
        "Muscu": "#6FA8DC",       # Bleu pastel
        "Danse": "#F7A8C4",       # Rose pastel
        "Escalade": "#9B8CFF",    # Violet pastel
        "Randonnée": "#7ED6C1",   # Vert menthe
        "Stretching": "#D85C7A",  # Framboise
        "Autre": "#C7CCD6"        # Gris bleuté pastel
    }

    fig = px.pie(
        df_repartition,
        names="Activite",
        values="Temps",
        hole=0.35,
        color="Activite",
        color_discrete_map=couleurs_activites
    )

    fig.update_traces(
        hovertemplate="%{label}<br>%{customdata}",
        customdata=df_repartition["Affichage"]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )



# ==========================
# Evolution du sport
# ==========================

st.subheader(
    "Evolution du temps de sport"
)


df_evolution = df_filtre.copy()


df_evolution["Total"] = (
    df_evolution[activites]
    .sum(axis=1)
)


# ==========================
# Couleurs fixes par année
# ==========================

couleurs_annees = {
    2021: "#7ED6C1",  # Vert menthe
    2022: "#6FA8DC",  # Bleu pastel
    2023: "#9B8CFF",  # Violet pastel
    2024: "#D85C7A",  # Framboise
    2025: "#F7A8C4",  # Rose pastel
    2026: "#F7C8A8"   # Pêche pastel
}


# ==========================
# Toutes les années = par mois
# ==========================

if annees_selection == "Toutes":


    df_evolution["Année"] = (
        df_evolution["Date"]
        .dt.year
    )


    df_evolution["Mois"] = (
        df_evolution["Date"]
        .dt.month
    )


    evolution = (
        df_evolution
        .groupby(
            [
                "Année",
                "Mois"
            ],
            as_index=False
        )["Total"]
        .sum()
    )


    mois_noms = [
        "",
        "Jan",
        "Fév",
        "Mar",
        "Avr",
        "Mai",
        "Juin",
        "Juil",
        "Août",
        "Sep",
        "Oct",
        "Nov",
        "Déc",
    ]


    evolution["Mois_nom"] = (
        evolution["Mois"]
        .apply(
            lambda x: mois_noms[x]
        )
    )


    fig_evolution = px.line(
        evolution,
        x="Mois_nom",
        y="Total",
        color="Année",
        markers=True,
        color_discrete_map=couleurs_annees,
        labels={
            "Mois_nom": "Mois",
            "Total": "Temps (minutes)",
            "Année": "Année"
        }
    )


    fig_evolution.update_layout(
        xaxis={
            "categoryorder": "array",
            "categoryarray": mois_noms[1:]
        }
    )


# ==========================
# Une année = par semaine
# ==========================

else:


    df_evolution["Semaine"] = (
        df_evolution["Date"]
        .dt.isocalendar()
        .week
        .astype(int)
    )


    evolution = (
        df_evolution
        .groupby(
            "Semaine",
            as_index=False
        )["Total"]
        .sum()
        .sort_values(
            "Semaine"
        )
    )


    fig_evolution = px.line(
        evolution,
        x="Semaine",
        y="Total",
        markers=True,
        labels={
            "Semaine": "Semaine",
            "Total": "Temps (minutes)"
        }
    )


    # Couleur fixe selon l'année sélectionnée
    fig_evolution.update_traces(
        line_color=couleurs_annees.get(
            annees_selection,
            "#C7CCD6"
        )
    )


# ==========================
# Affichage
# ==========================

st.plotly_chart(
    fig_evolution,
    use_container_width=True
)



# ==========================
# Tableau détaillé
# ==========================

st.subheader(
    "Détail quotidien"
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


df_affichage = df_affichage[
    colonnes
]


st.dataframe(
    df_affichage,
    use_container_width=True,
    hide_index=True
)
