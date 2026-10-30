
import streamlit as st
import pandas as pd
from html import escape

from scripts.musique.google_sheet import charger_musique

# ==========================
# CONFIGURATION
# ==========================

st.set_page_config(
    page_title="Tous mes albums",
    layout="wide"
)

st.title("💿 Tous mes albums")

# ==========================
# CSS : GRILLE RESPONSIVE
# ==========================

st.markdown(
    """
    <style>

    /* Grille des albums */

    div[data-testid="stHorizontalBlock"]:has(
        div[data-testid="column"] .album-card
    ) {
        display: grid !important;
        grid-template-columns: repeat(6, minmax(0, 1fr));
        gap: 20px 12px;
    }

    div[data-testid="stHorizontalBlock"]:has(
        div[data-testid="column"] .album-card
    ) > div[data-testid="column"] {
        width: 100% !important;
        min-width: 0 !important;
        flex: unset !important;
    }

    /* Tablettes */

    @media (max-width: 900px) {
        div[data-testid="stHorizontalBlock"]:has(
            div[data-testid="column"] .album-card
        ) {
            grid-template-columns: repeat(4, minmax(0, 1fr));
        }
    }

    /* Téléphones */

    @media (max-width: 600px) {
        div[data-testid="stHorizontalBlock"]:has(
            div[data-testid="column"] .album-card
        ) {
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 16px 8px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==========================
# CHARGEMENT DES DONNÉES
# ==========================

df_albums = charger_musique().copy()

# ==========================
# NETTOYAGE
# ==========================

df_albums["Date"] = pd.to_datetime(
    df_albums["Date"],
    errors="coerce"
)

df_albums["Annee_ecoute"] = df_albums["Date"].dt.year

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
# FILTRES ET TRI
# ==========================

col1, col2, col3, col4, col5, col6 = st.columns(
    [1, 1, 1, 1, 1, 1.8]
)

with col1:

    critere_tri = st.selectbox(
        "Trier par",
        ["Date", "Note", "Artiste"]
    )

with col2:

    ordre_tri = st.selectbox(
        "Ordre",
        ["Décroissant", "Croissant"]
    )

with col3:

    pays_disponibles = sorted(
        [p for p in df_albums["Pays"].unique() if p]
    )

    pays_selectionne = st.selectbox(
        "Pays",
        ["Tous"] + pays_disponibles
    )

with col4:

    styles_disponibles = sorted(
        [s for s in df_albums["Genre (large)"].unique() if s]
    )

    style_selectionne = st.selectbox(
        "Style",
        ["Tous"] + styles_disponibles
    )

with col5:

    annees = sorted(
        df_albums["Annee_ecoute"]
        .dropna()
        .astype(int)
        .unique(),
        reverse=True
    )

    annee_selectionnee = st.selectbox(
        "Année d'écoute",
        ["Toutes"] + annees
    )

with col6:

    recherche = st.text_input(
        "Rechercher",
        placeholder="Album ou artiste..."
    )

# ==========================
# APPLICATION DES FILTRES
# ==========================

df_filtre = df_albums.copy()

# Filtre pays

if pays_selectionne != "Tous":

    df_filtre = df_filtre[
        df_filtre["Pays"] == pays_selectionne
    ]

# Filtre style

if style_selectionne != "Tous":

    df_filtre = df_filtre[
        df_filtre["Genre (large)"] == style_selectionne
    ]

# Filtre année

if annee_selectionnee != "Toutes":

    df_filtre = df_filtre[
        df_filtre["Annee_ecoute"] == int(annee_selectionnee)
    ]

# Recherche album ou artiste

if recherche.strip():

    masque = (
        df_filtre["spotify_album"]
        .fillna("")
        .astype(str)
        .str.contains(
            recherche.strip(),
            case=False,
            na=False,
            regex=False
        )
        |
        df_filtre["spotify_artiste"]
        .fillna("")
        .astype(str)
        .str.contains(
            recherche.strip(),
            case=False,
            na=False,
            regex=False
        )
    )

    df_filtre = df_filtre[masque]

# ==========================
# APPLICATION DU TRI
# ==========================

ascending = ordre_tri == "Croissant"

if critere_tri == "Date":

    df_filtre = df_filtre.sort_values(
        by="Date",
        ascending=ascending,
        na_position="last"
    )

elif critere_tri == "Note":

    df_filtre = df_filtre.sort_values(
        by="Note",
        ascending=ascending,
        na_position="last"
    )

elif critere_tri == "Artiste":

    df_filtre = df_filtre.sort_values(
        by="spotify_artiste",
        ascending=ascending,
        na_position="last",
        key=lambda s: s.str.lower()
    )

# ==========================
# NOMBRE D'ALBUMS
# ==========================

st.caption(f"{len(df_filtre)} album(s)")

st.divider()

# ==========================
# GRILLE DES ALBUMS
# ==========================

NB_COLONNES = 6

for i in range(0, len(df_filtre), NB_COLONNES):

    elements_ligne = df_filtre.iloc[
        i:i + NB_COLONNES
    ]

    colonnes = st.columns(NB_COLONNES)

    for col, (_, album) in zip(
        colonnes,
        elements_ligne.iterrows()
    ):

        with col:

            # --------------------------
            # POCHETTE
            # --------------------------

            cover_url = album.get(
                "cover_url",
                ""
            )

            if (
                pd.notna(cover_url)
                and str(cover_url).strip()
            ):

                st.image(
                    str(cover_url).strip(),
                    use_container_width=True
                )

            else:

                st.markdown(
                    """
                    <div style="
                        width:100%;
                        aspect-ratio:1/1;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        text-align:center;
                        background-color:rgba(128,128,128,0.12);
                        border-radius:5px;
                        color:gray;
                        font-size:12px;
                    ">
                        💿 Pas de pochette
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # --------------------------
            # TITRE
            # --------------------------

            titre = escape(
                str(album.get("spotify_album", "Sans titre"))
            )

            st.markdown(
                f"""
                <div class="album-card" style="
                    text-align:center;
                    font-size:13px;
                    font-weight:600;
                    line-height:1.2;
                    overflow-wrap:anywhere;
                ">
                    {titre}
                </div>
                """,
                unsafe_allow_html=True
            )

            # --------------------------
            # ARTISTE ET NOTE
            # --------------------------

            artiste = escape(
                str(album.get("spotify_artiste", ""))
            )

            note = album.get("Note")

            if pd.notna(note):

                note_affichee = f"⭐ {int(note)}/10"

            else:

                note_affichee = ""

            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    font-size:11px;
                    color:gray;
                    line-height:1.2;
                    overflow-wrap:anywhere;
                ">
                    {artiste}
                    {" · " + note_affichee if note_affichee else ""}
                </div>
                """,
                unsafe_allow_html=True
            )
