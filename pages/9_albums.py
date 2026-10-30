
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
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
# FILTRES ET TRI RESPONSIVES
# ==========================

st.markdown(
    """
    <style>
    /* Filtres sur une seule ligne sur ordinateur */
    @media (min-width: 901px) {
        div[data-testid="stHorizontalBlock"]:has(
            [data-testid="stSelectbox"],
            [data-testid="stTextInput"]
        ) {
            flex-wrap: nowrap !important;
        }
    }

    /* Deux colonnes sur téléphone */
    @media (max-width: 600px) {
        div[data-testid="stHorizontalBlock"]:has(
            [data-testid="stSelectbox"],
            [data-testid="stTextInput"]
        ) {
            display: grid !important;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 10px !important;
        }

        div[data-testid="stHorizontalBlock"]:has(
            [data-testid="stSelectbox"],
            [data-testid="stTextInput"]
        ) > div[data-testid="column"] {
            width: 100% !important;
            min-width: 0 !important;
            flex: unset !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

if pays_selectionne != "Tous":
    df_filtre = df_filtre[
        df_filtre["Pays"] == pays_selectionne
    ]

if style_selectionne != "Tous":
    df_filtre = df_filtre[
        df_filtre["Genre (large)"] == style_selectionne
    ]

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
# CONSTRUCTION DES CARTES HTML
# ==========================

cartes = []

for _, album in df_filtre.iterrows():

    cover_url = album.get("cover_url", "")

    titre = escape(
        str(album.get("spotify_album", "Sans titre"))
    )

    artiste = escape(
        str(album.get("spotify_artiste", ""))
    )

    note = album.get("Note")

    if pd.notna(note):
        note_affichee = f"⭐ {int(note)}/10"
    else:
        note_affichee = ""

    # Pochette
    if pd.notna(cover_url) and str(cover_url).strip():

        image_html = f"""
            <img
                src="{escape(str(cover_url).strip(), quote=True)}"
                alt="{titre}"
            >
        """

    else:

        image_html = """
            <div class="image-vide">
                💿 Pas de pochette
            </div>
        """

    cartes.append(f"""
        <div class="album">

            {image_html}

            <div class="titre">
                {titre}
            </div>

            <div class="infos">
                {artiste}
                {" · " + note_affichee if note_affichee else ""}
            </div>

        </div>
    """)

# ==========================
# CONSTRUCTION HTML
# ==========================

html_page = f"""
<!DOCTYPE html>
<html>
<head>

<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

* {{
    box-sizing: border-box;
}}

html, body {{
    margin: 0;
    padding: 0;
    font-family: sans-serif;
    background: transparent;
    color: #FFFFFF;
}}

.grille {{
    display: grid;
    grid-template-columns: repeat(6, minmax(0, 1fr));
    gap: 20px 12px;
    width: 100%;
}}

.album {{
    min-width: 0;
}}

.album img,
.image-vide {{
    display: block;
    width: 100%;
    aspect-ratio: 1 / 1;
    object-fit: cover;
    border-radius: 5px;
}}

.image-vide {{
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: rgba(128, 128, 128, 0.2);
    color: #FFFFFF;
    font-size: 12px;
}}

.titre {{
    margin-top: 7px;
    font-size: 13px;
    font-weight: 600;
    line-height: 1.35;
    overflow-wrap: anywhere;
    color: #FFFFFF;
}}

.infos {{
    margin-top: 3px;
    font-size: 11px;
    line-height: 1.4;
    overflow-wrap: anywhere;
    color: #FFFFFF;
    opacity: 0.75;
}}

/* Tablettes */

@media (max-width: 900px) {{

    .grille {{
        grid-template-columns: repeat(4, minmax(0, 1fr));
    }}

}}

/* Téléphones */

@media (max-width: 600px) {{

    .grille {{
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 16px 8px;
    }}

    .titre {{
        font-size: 12px;
    }}

    .infos {{
        font-size: 10px;
    }}

}}

</style>
</head>

<body>

<div class="grille">
    {''.join(cartes)}
</div>

</body>
</html>
"""

# ==========================
# AFFICHAGE
# ==========================

# Hauteur estimée pour 3 colonnes sur téléphone
nb_lignes = (len(df_filtre) + 2) // 3

hauteur = max(100, nb_lignes * 220)

components.html(
    html_page,
    height=hauteur,
    scrolling=False
)
