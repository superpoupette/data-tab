import streamlit as st
import pandas as pd

from scripts.musique.google_sheet import charger_musique

st.set_page_config(
    page_title="Tous mes albums",
    layout="wide"
)

st.title("💿 Tous mes albums")

df_albums = charger_musique()

# ==========================
# Nettoyage
# ==========================

df_albums["Date"] = pd.to_datetime(
    df_albums["Date"],
    errors="coerce"
)

df_albums["Note"] = (
    df_albums["Note"]
    .astype(str)
    .str.replace(",", ".", regex=False)
)

df_albums["Note"] = pd.to_numeric(
    df_albums["Note"],
    errors="coerce"
)

# Nettoyage pays / styles
df_albums["Pays"] = (
    df_albums["Pays"]
    .fillna("")
    .astype(str)
    .str.strip()
)

df_albums["Genre (large)"] = (
    df_albums["Genre (large)"]
    .fillna("")
    .astype(str)
    .str.strip()
)

# ==========================
# Filtres et tri
# ==========================

col1, col2, col3, col4 = st.columns(4)

with col1:

    critere_tri = st.selectbox(
        "Trier par",
        [
            "Date",
            "Note"
        ]
    )

with col2:

    ordre_tri = st.selectbox(
        "Ordre",
        [
            "Décroissant",
            "Croissant"
        ]
    )

with col3:

    pays_disponibles = sorted(
        [
            pays
            for pays in df_albums["Pays"].unique()
            if pays
        ]
    )

    pays_selectionne = st.selectbox(
        "Pays",
        ["Tous"] + pays_disponibles
    )

with col4:

    styles_disponibles = sorted(
        [
            style
            for style in df_albums["Genre (large)"].unique()
            if style
        ]
    )

    style_selectionne = st.selectbox(
        "Style",
        ["Tous"] + styles_disponibles
    )


# ==========================
# Application des filtres
# ==========================

df_filtre = df_albums.copy()

if pays_selectionne != "Tous":
    df_filtre = df_filtre[
        df_filtre["Pays"] == pays_selectionne
    ]

if style_selectionne != "Tous":
    df_filtre = df_filtre[
        df_filtre["Genre (large)"] == style_selectionne
    ]


# ==========================
# Application du tri
# ==========================

ascending = ordre_tri == "Croissant"

df_filtre = df_filtre.sort_values(
    critere_tri,
    ascending=ascending,
    na_position="last"
)


# ==========================
# Nombre d'albums
# ==========================

st.caption(
    f"{len(df_filtre)} album(s)"
)


# ==========================
# Grille des albums
# ==========================

NB_COLONNES = 6

for i in range(0, len(df_filtre), NB_COLONNES):

    albums_ligne = df_filtre.iloc[
        i:i + NB_COLONNES
    ]

    cols = st.columns(NB_COLONNES)

    for col, (_, album) in zip(
        cols,
        albums_ligne.iterrows()
    ):

        with col:

            # Pochette
            if (
                pd.notna(album["cover_url"])
                and album["cover_url"]
            ):
                st.image(
                    album["cover_url"],
                    use_container_width=True
                )

            # Nom de l'album
            st.markdown(
                f"**{album['spotify_album']}**"
            )

            # Artiste + note
            if pd.notna(album["Note"]):
                note_affichee = (
                    f"⭐ {int(album['Note'])}/10"
                )
            else:
                note_affichee = "⭐ Sans note"

            st.caption(
                f"{album['spotify_artiste']} · "
                f"{note_affichee}"
            )