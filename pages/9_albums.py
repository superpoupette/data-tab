import streamlit as st
import pandas as pd
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
# Grille responsive des albums
# ==========================

cartes = []

for _, album in df_filtre.iterrows():

    # Pochette
    cover_url = (
        str(album["cover_url"])
        if pd.notna(album["cover_url"])
        else ""
    )

    # Nom de l'album et artiste
    nom_album = escape(str(album["spotify_album"]))
    artiste = escape(str(album["spotify_artiste"]))

    # Note
    if pd.notna(album["Note"]):
        note_affichee = f"⭐ {int(album['Note'])}/10"
    else:
        note_affichee = "⭐ Sans note"

    # Carte
    if cover_url:
        image_html = f"""
            <img
                src="{escape(cover_url, quote=True)}"
                alt="{nom_album}"
                loading="lazy"
            >
        """
    else:
        image_html = """
            <div class="image-vide"></div>
        """

    cartes.append(f"""
        <div class="album">
            {image_html}
            <div class="titre">{nom_album}</div>
            <div class="infos">{artiste} · {note_affichee}</div>
        </div>
    """)

# ==========================
# Thème et couleurs Streamlit
# ==========================

theme = st.get_option("theme.base")

if theme == "dark":
    couleur_titre = "#FFFFFF"
    couleur_infos = "#E0E0E0"
    couleur_fond = "#0E1117"
else:
    couleur_titre = "#000000"
    couleur_infos = "#555555"
    couleur_fond = "#FFFFFF"

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
        color: {couleur_texte};
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
        color: {couleur_texte};
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
        background: {couleur_fond};
        opacity: 0.15;
    }}

    .titre {{
        margin-top: 7px;
        font-size: 13px;
        font-weight: 600;
        line-height: 1.35;
        overflow-wrap: anywhere;
        color: {couleur_texte};
    }}

    .infos {{
        margin-top: 3px;
        font-size: 11px;
        line-height: 1.4;
        opacity: 0.75;
        overflow-wrap: anywhere;
        color: {couleur_texte};
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

components.html(
    html,
    height=hauteur,
    scrolling=False
)
