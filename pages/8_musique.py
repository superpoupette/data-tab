import streamlit as st
import plotly.express as px

from scripts.importation_spotify import charger_historique_spotify
from scripts.musique.google_sheet import charger_musique

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

heures_ecoute = df_filtre["minutes"].sum() / 60

c2.metric(
    "Heures d'écoute",
    f"{heures_ecoute:.1f} h"
)

c3.metric(
    "Artistes",
    df_filtre["master_metadata_album_artist_name"].nunique()
)

c4.metric(
    "Morceaux différents",
    df_filtre["master_metadata_track_name"].nunique()
)

st.divider()


# ------------------------
# Deux colonnes
# ------------------------

col1, col2 = st.columns(2)

with col1:

    top_artistes = (
        df_filtre
        .groupby("master_metadata_album_artist_name")["minutes"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_artistes,
        x="minutes",
        y="master_metadata_album_artist_name",
        orientation="h",
        text_auto=".1f",
        title="Top 10 des artistes"
    )

    fig.update_layout(
        yaxis_title="",
        xaxis_title="Minutes d'écoute",
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    top_titres = (
        df_filtre
        .groupby("master_metadata_track_name")["minutes"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_titres,
        x="minutes",
        y="master_metadata_track_name",
        orientation="h",
        text_auto=".1f",
        title="Top 10 des morceaux"
    )

    fig.update_layout(
        yaxis_title="",
        xaxis_title="Minutes d'écoute",
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig, use_container_width=True)


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


st.divider()

st.subheader("💿 Collection d'albums")
df_albums = charger_musique()

st.divider()

# ==========================
# 5 derniers albums écoutés
# ==========================

st.subheader("🆕 Derniers albums écoutés")

derniers = (
    df_albums
    .sort_values("Date", ascending=False)
    .head(5)
)

cols = st.columns(5)

for col, (_, album) in zip(cols, derniers.iterrows()):

    with col:

        if album["cover_url"]:
            st.image(album["cover_url"])

        st.markdown(
            f"**{album['spotify_album']}**\n\n"
            f"{album['spotify_artiste']}"
        )

st.divider()

# ==========================
# Albums préférés
# ==========================

st.subheader("❤️ Albums préférés")

favoris = (
    df_albums
    .sort_values(["Note", "Date"], ascending=[False, False])
    .head(5)
)

cols = st.columns(5)

for col, (_, album) in zip(cols, favoris.iterrows()):

    with col:

        if album["cover_url"]:
            st.image(album["cover_url"])

        st.markdown(
            f"**{album['spotify_album']}**\n\n"
            f"{album['spotify_artiste']}"
        )

st.divider()

st.header("💿 Ma bibliothèque musicale")



st.dataframe(
    df_albums,
    use_container_width=True,
    hide_index=True
)