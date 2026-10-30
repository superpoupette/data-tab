
import streamlit as st
import pandas as pd
import html
import streamlit.components.v1 as components
from html import escape
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
# Filtres et tri
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

if annee_selectionnee != "Toutes":
    df_filtre = df_filtre[
        df_filtre["Annee_ecoute"] == int(annee_selectionnee)
    ]

# Recherche album ou artiste
if recherche:
    masque = (
        df_filtre["spotify_album"]
        .fillna("")
        .str.contains(recherche, case=False, na=False)
        |
        df_filtre["spotify_artiste"]
        .fillna("")
        .str.contains(recherche, case=False, na=False)
    )

    df_filtre = df_filtre[masque]

# ==========================
# Application du tri
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
# Nombre d'albums
# ==========================

st.caption(f"{len(df_filtre)} album(s)")

# ==========================
# GRILLE DES ALBUMS
# ==========================

NB_COLONNES = 6

for i in range(0, len(df_filtre), NB_COLONNES):

    elements_ligne = df_filtre.iloc[i:i + NB_COLONNES]

    colonnes = st.columns(NB_COLONNES)

    for col, (_, album) in zip(colonnes, elements_ligne.iterrows()):

        with col:

            # Pochette
            cover_url = album.get("cover_url", "")

            if pd.notna(cover_url) and str(cover_url).strip():

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

            # Titre
            titre = html.escape(
                str(album.get("spotify_album", "Sans titre"))
            )

            st.markdown(
                f"""
                <div style="
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

            # Artiste et note
            artiste = html.escape(
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
                    {artiste} {" · " + note_affichee if note_affichee else ""}
                </div>
                """,
                unsafe_allow_html=True
            )

# ==========================
# Construction HTML
# ==========================

html = f"""
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
        background: transparent;
    }}

    .titre {{
        margin-top: 7px;
        font-size: 13px;
        font-weight: 600;
        line-height: 1.35;
        overflow-wrap: anywhere;
    }}

    .infos {{
        margin-top: 3px;
        font-size: 11px;
        line-height: 1.4;
        overflow-wrap: anywhere;
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
# Affichage
# ==========================

# Hauteur estimée : 3 colonnes sur téléphone
nb_lignes = (len(df_filtre) + 2) // 3

hauteur = max(100, nb_lignes * 220)

