import streamlit as st
import pandas as pd

from scripts.musique.google_sheet import charger_musique

st.set_page_config(
    page_title="Tous mes albums",
    layout="wide"
)

st.title("💿 Tous mes albums")

df_albums = charger_musique()

# Nettoyage
df_albums["Date"] = pd.to_datetime(
    df_albums["Date"],
    errors="coerce"
)

# Nombre de colonnes dans la grille
NB_COLONNES = 6

for i in range(0, len(df_albums), NB_COLONNES):

    albums_ligne = df_albums.iloc[i:i + NB_COLONNES]

    cols = st.columns(NB_COLONNES)

    for col, (_, album) in zip(cols, albums_ligne.iterrows()):

        with col:

            if pd.notna(album["cover_url"]) and album["cover_url"]:
                st.image(
                    album["cover_url"],
                    use_container_width=True
                )

            st.markdown(
                f"**{album['spotify_album']}**"
            )

            st.caption(
                album["spotify_artiste"]
            )