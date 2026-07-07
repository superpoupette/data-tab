import streamlit as st
import pandas as pd
import plotly.express as px

from scripts.importation_2024 import prepare_2024
from scripts.importation_2025 import prepare_2025
from scripts.gestion_danses import create_danse_data
from scripts.gestion_danses import create_danse_recap


# Chargement des données

data2024 = prepare_2024(
    "data/2024.csv"
)

data2025 = prepare_2025(
    "data/2025.csv"
)


danse_2024 = create_danse_data(data2024)
danse_2025 = create_danse_data(data2025)


danse_data = pd.concat(
    [
        danse_2024,
        danse_2025
    ],
    ignore_index=True
)


danse_recap = create_danse_recap(danse_data)


st.title("Dashboard Danse")


# =========================
# Indicateurs principaux
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    temps_total_min = danse_data["duree_min"].sum()

    heures = int(temps_total_min // 60)
    minutes = int(temps_total_min % 60)

    st.metric(
        "Temps d'apprentissage global",
        f"{heures}h{minutes:02d}"
    )

with col2:
    nb_chorees = (
        danse_recap["duree_apprentissage"] > 0
    ).sum()

    st.metric(
        "Nombre de chorégraphies apprises",
        nb_chorees
    )

with col3:
    nb_sessions = danse_data["date"].nunique()

    st.metric(
        "Nombre de sessions de danse",
        nb_sessions
    )

with col4:
    duree_moyenne = (
        danse_data
        .groupby("date")["duree_min"]
        .sum()
        .mean()
    )

    st.metric(
        "Durée moyenne d'une session",
        f"{duree_moyenne:.0f} min"
    )


# =========================
# Préparation des données
# =========================

danse_data["mois"] = (
    pd.to_datetime(danse_data["date"])
    .dt.to_period("M")
    .astype(str)
)


# =========================
# Graphiques principaux
# =========================

col1, col2 = st.columns(2)


# Répartition des styles

with col1:
    st.subheader("Répartition des styles")

    styles = (
        danse_recap
        .groupby("Style")
        .size()
        .reset_index(name="nombre")
    )

    fig_style = px.pie(
        styles,
        values="nombre",
        names="Style",
        hole=0.3
    )

    st.plotly_chart(
        fig_style,
        use_container_width=True
    )


# Répartition par artiste

# Top artistes par nombre de chorégraphies

with col2:
    st.subheader("Top 10 artistes par nombre de chorégraphies")

    artistes = (
        danse_recap[danse_recap["duree_apprentissage"] > 0]
        .groupby("artiste")
        .size()
        .reset_index(name="nombre_chorees")
        .sort_values(
            "nombre_chorees",
            ascending=False
        )
        .head(10)
        .reset_index(drop=True)
    )

    st.dataframe(
        artistes,
        use_container_width=True,
        hide_index=True
    )

# =========================
# Evolution mensuelle
# =========================

st.subheader("Temps d'apprentissage par mois")

temps_mois = (
    danse_data
    .groupby("mois", as_index=False)["duree_min"]
    .sum()
)

fig_mois = px.line(
    temps_mois,
    x="mois",
    y="duree_min",
    markers=True,
    labels={
        "mois": "Mois",
        "duree_min": "Temps (min)"
    }
)

st.plotly_chart(
    fig_mois,
    use_container_width=True
)


# =========================
# Top chorégraphies
# =========================

st.subheader("Top 10 des chorégraphies par temps d'apprentissage")

top_chorees = (
    danse_recap
    .sort_values(
        "duree_apprentissage",
        ascending=False
    )
    .head(10)
)


fig_top = px.bar(
    top_chorees,
    y="titre",
    x="duree_apprentissage",
    orientation="h",
    labels={
        "titre": "Chorégraphie",
        "duree_apprentissage": "Temps (min)"
    }
)

st.plotly_chart(
    fig_top,
    use_container_width=True
)


# =========================
# Tableau récapitulatif
# =========================

st.subheader("Récapitulatif des chorégraphies")

st.dataframe(
    danse_recap,
    use_container_width=True
)