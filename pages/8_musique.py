import streamlit as st
import plotly.express as px

from scripts.importation_spotify import charger_historique_spotify

st.set_page_config(page_title="Musique", layout="wide")

st.title("🎵 Spotify Dashboard")

df = charger_historique_spotify()

# ------------------------
# KPIs
# ------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Titres écoutés",
    f"{len(df):,}".replace(",", " ")
)

c2.metric(
    "Heures d'écoute",
    f"{df['minutes'].sum()/60:.1f}"
)

c3.metric(
    "Artistes",
    df["master_metadata_album_artist_name"].nunique()
)

c4.metric(
    "Morceaux différents",
    df["master_metadata_track_name"].nunique()
)

st.divider()

# ------------------------
# Temps d'écoute mensuel
# ------------------------

ecoute_mois = (
    df.groupby("mois")["minutes"]
    .sum()
    .reset_index()
)

fig = px.line(
    ecoute_mois,
    x="mois",
    y="minutes",
    markers=True,
    title="Temps d'écoute par mois"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------
# Deux colonnes
# ------------------------

col1, col2 = st.columns(2)

with col1:

    top_artistes = (
        df.groupby("master_metadata_album_artist_name")
        ["minutes"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    fig = px.bar(
        top_artistes,
        x="minutes",
        y="master_metadata_album_artist_name",
        orientation="h",
        title="Top artistes"
    )

    fig.update_layout(yaxis={"categoryorder": "total ascending"})

    st.plotly_chart(fig, use_container_width=True)

with col2:

    top_titres = (
        df.groupby("master_metadata_track_name")
        ["minutes"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    fig = px.bar(
        top_titres,
        x="minutes",
        y="master_metadata_track_name",
        orientation="h",
        title="Top morceaux"
    )

    fig.update_layout(yaxis={"categoryorder": "total ascending"})

    st.plotly_chart(fig, use_container_width=True)

