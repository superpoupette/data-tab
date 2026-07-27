import streamlit as st
import plotly.express as px

from scripts.importation_spotify import charger_historique_spotify

st.set_page_config(page_title="Musique", layout="wide")

st.title("🎵 Spotify Dashboard")

df = charger_historique_spotify()

# ------------------------
# Filtres
# ------------------------

col_filtre1, col_filtre2 = st.columns(2)

annees = ["Toutes"] + sorted(df["année"].unique().tolist())

annee = col_filtre1.selectbox(
    "Année",
    annees
)

if annee != "Toutes":
    df_filtre = df[df["année"] == annee]
else:
    df_filtre = df.copy()

mois = ["Tous"] + sorted(df_filtre["mois"].unique().tolist())

mois_selectionne = col_filtre2.selectbox(
    "Mois",
    mois
)

if mois_selectionne != "Tous":
    df_filtre = df_filtre[df_filtre["mois"] == mois_selectionne]


# ------------------------
# KPIs
# ------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Titres écoutés",
    f"{len(df_filtre):,}".replace(",", " ")
)

jours_ecoute = df["minutes"].sum() / 60 / 24

c2.metric(
    "Jours d'écoute",
    f"{jours_ecoute:.1f}"
)
c3.metric(
    "Artistes",
    df_filtre["master_metadata_album_artist_name"].nunique()
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
    df_filtre.groupby("mois")["minutes"]
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
        df_filtre
        .groupby("master_metadata_album_artist_name")
        .agg(
            Ecoutes=("master_metadata_track_name", "count"),
            Minutes=("minutes", "sum"),
            Titres=("master_metadata_track_name", "nunique")
        )
        .sort_values("Minutes", ascending=False)
        .reset_index()
    )

    top_artistes["Jours"] = (top_artistes["Minutes"] / 60 / 24).round(2)

    top_artistes = top_artistes.rename(columns={
        "master_metadata_album_artist_name": "Artiste"
    })

    st.subheader("Top artistes")

    st.dataframe(
        top_artistes[
            ["Artiste", "Ecoutes", "Titres", "Jours"]
        ],
        use_container_width=True,
        hide_index=True
    )

with col2:

    top_titres = (
        df_filtre.groupby("master_metadata_track_name")
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

