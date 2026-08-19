import streamlit as st
import plotly.express as px
import pandas as pd

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
# ==========================
# Chargement bibliothèque albums
# ==========================

df_albums = charger_musique()

# Conversion date
df_albums["Date"] = pd.to_datetime(
    df_albums["Date"],
    errors="coerce"
)

# Nettoyage des notes
df_albums["Note"] = (
    df_albums["Note"]
    .astype(str)
    .str.replace(",", ".", regex=False)
)

df_albums["Note"] = pd.to_numeric(
    df_albums["Note"],
    errors="coerce"
)

# ==========================
# Albums préférés
# ==========================

st.subheader("Albums préférés")


df_notes = (
    df_albums
    .dropna(subset=["Note"])
    .copy()
)


favoris = (
    df_notes
    .sort_values(
        ["Note", "Date"],
        ascending=[False, False]
    )
    .head(5)
)


cols = st.columns(5)


for col, (_, album) in zip(cols, favoris.iterrows()):

    with col:

        if album["cover_url"]:
            st.image(
                album["cover_url"],
                use_container_width=True
            )

        note_affichee = (
            f"⭐ {int(album['Note'])}"
            if pd.notna(album["Note"])
            else "⭐ Sans note"
        )

        st.markdown(
            f"**{album['spotify_album']}**\n\n"
            f"{album['spotify_artiste']}\n\n"
            f"{note_affichee}"
        )


st.divider()


# ==========================
# 5 derniers albums écoutés
# ==========================

st.subheader("Derniers albums écoutés")


derniers = (
    df_albums
    .sort_values(
        "Date",
        ascending=False
    )
    .head(5)
)


cols = st.columns(5)


for col, (_, album) in zip(cols, derniers.iterrows()):

    with col:

        if album["cover_url"]:
            st.image(
                album["cover_url"],
                use_container_width=True
            )

        note_affichee = (
            f"⭐ {int(album['Note'])}"
            if pd.notna(album["Note"])
            else "⭐ Sans note"
        )

        st.markdown(
            f"**{album['spotify_album']}**\n\n"
            f"{album['spotify_artiste']}\n\n"
            f"{note_affichee}"
        )

if st.button("Voir tous les albums"):
    st.switch_page("pages/albums.py")

# ==========================
# Statistiques bibliothèque
# ==========================

st.divider()

st.header("Statistiques de ma bibliothèque")


col1, col2 = st.columns(2)


# ==========================
# Répartition des genres
# ==========================

with col1:

    genres = (
        df_albums["Genre (large)"]
        .replace("", "Non renseigné")
        .fillna("Non renseigné")
        .value_counts()
        .reset_index()
    )

    genres.columns = [
        "Genre",
        "Nombre"
    ]

    fig_genres = px.pie(
        genres,
        names="Genre",
        values="Nombre",
        title="Répartition des genres",
        hole=0.3
    )

    st.plotly_chart(
        fig_genres,
        use_container_width=True
    )


# ==========================
# Répartition des pays
# ==========================

with col2:

    pays = (
        df_albums["Pays"]
        .replace("", "Non renseigné")
        .fillna("Non renseigné")
        .value_counts()
        .reset_index()
    )

    pays.columns = [
        "Pays",
        "Nombre"
    ]

    fig_pays = px.pie(
        pays,
        names="Pays",
        values="Nombre",
        title="Répartition des pays",
        hole=0.3
    )

    st.plotly_chart(
        fig_pays,
        use_container_width=True
    )


# ==========================
# Répartition des notes
# ==========================

notes = (
    df_albums
    .dropna(subset=["Note"])
    .copy()
)


notes["Note"] = notes["Note"].astype(float)


repartition_notes = (
    notes["Note"]
    .value_counts()
    .sort_index()
    .reset_index()
)


repartition_notes.columns = [
    "Note",
    "Nombre"
]


fig_notes = px.bar(
    repartition_notes,
    x="Note",
    y="Nombre",
    text="Nombre",
    title="Répartition des notes",
)


fig_notes.update_layout(
    xaxis_title="Note / 10",
    yaxis_title="Nombre d'albums",
    xaxis=dict(
        dtick=1,
        range=[-0.5, 10.5]
    )
)


st.plotly_chart(
    fig_notes,
    use_container_width=True
)
