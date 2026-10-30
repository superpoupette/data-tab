import streamlit as st
import pandas as pd
import html

import streamlit.components.v1 as components

from scripts.watchlist.load_watchlist import (
    load_movies_google_sheet,
    load_series_google_sheet
)

# ==========================
# CONFIGURATION
# ==========================

st.set_page_config(
    page_title="Toutes mes affiches",
    page_icon="🍿",
    layout="wide"
)

st.title("🍿 Toutes mes affiches")


# ==========================
# CHARGEMENT DES DONNÉES
# ==========================

@st.cache_data(ttl=300)
def charger_donnees():

    movies = load_movies_google_sheet().copy()
    series_all = load_series_google_sheet().copy()

    # Normalisation des types
    if "type" not in series_all.columns:
        series_all["type"] = "series"

    series_all["type"] = (
        series_all["type"]
        .fillna("series")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Ajout du type pour les films
    movies["type"] = "movie"

    # Harmonisation des dates
    for df, colonnes in [
        (movies, ["watched_at"]),
        (series_all, ["last_watch"])
    ]:
        for colonne in colonnes:
            if colonne in df.columns:
                df[colonne] = pd.to_datetime(
                    df[colonne],
                    errors="coerce"
                )

    # Harmonisation des notes des films
    if "rating" in movies.columns:
        movies["rating"] = pd.to_numeric(
            movies["rating"],
            errors="coerce"
        )

    # Colonnes communes
    for df in [movies, series_all]:

        for colonne in [
            "title",
            "status",
            "poster_path",
            "style"
        ]:
            if colonne not in df.columns:
                df[colonne] = ""

            df[colonne] = (
                df[colonne]
                .fillna("")
                .astype(str)
                .str.strip()
            )

    # Colonnes propres aux films
    if "watched_at" not in movies.columns:
        movies["watched_at"] = pd.NaT

    if "rating" not in movies.columns:
        movies["rating"] = pd.NA

    if "watched_at" not in series_all.columns:
        series_all["watched_at"] = pd.NaT

    if "last_watch" not in series_all.columns:
        series_all["last_watch"] = pd.NaT

    # Harmonisation des dates d'affichage
    movies["date_affichage"] = movies["watched_at"]
    series_all["date_affichage"] = series_all["last_watch"]

    # Harmonisation des notes
    movies["note_affichage"] = movies["rating"]
    series_all["note_affichage"] = pd.NA

    # Harmonisation des statuts
    movies["statut_affichage"] = movies["status"]
    series_all["statut_affichage"] = series_all["status"]

    # Fusion des films, séries et animés
    df = pd.concat(
        [movies, series_all],
        ignore_index=True,
        sort=False
    )

    # Libellés des types
    types = {
        "movie": "Film",
        "series": "Série",
        "anime": "Animé"
    }

    df["type_affichage"] = (
        df["type"]
        .map(types)
        .fillna("Autre")
    )

    # Libellés des statuts
    statuts = {
        "watched": "Vu",
        "to_watch": "À voir",
        "continuing": "En cours",
        "up_to_date": "À jour",
        "stopped": "Stoppé"
    }

    df["statut_libelle"] = (
        df["statut_affichage"]
        .map(statuts)
        .fillna(df["statut_affichage"])
    )

    return df


df_affiches = charger_donnees()


# ==========================
# FILTRES RESPONSIVES
# ==========================

st.markdown(
    """
    <style>

    /* Ordinateur : filtres sur une seule ligne */
    @media (min-width: 901px) {
        div[data-testid="stHorizontalBlock"]:has(
            [data-testid="stSelectbox"],
            [data-testid="stTextInput"]
        ) {
            flex-wrap: nowrap !important;
        }
    }

    /* Téléphone : 2 lignes de filtres */
    @media (max-width: 600px) {

        div[data-testid="stHorizontalBlock"]:has(
            [data-testid="stSelectbox"],
            [data-testid="stTextInput"]
        ) {
            display: grid !important;
            grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
            gap: 8px !important;
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


col1, col2, col3, col4, col5 = st.columns(
    [1.3, 1.2, 1, 1.2, 2]
)

with col1:

    critere_tri = st.selectbox(
        "Trier par",
        [
            "Date de visionnage",
            "Titre",
            "Note"
        ]
    )

with col2:

    ordre_tri = st.selectbox(
        "Ordre de tri",
        [
            "Décroissant",
            "Croissant"
        ]
    )

with col3:

    type_selectionne = st.selectbox(
        "Type",
        [
            "Tous",
            "Film",
            "Série",
            "Animé"
        ]
    )

with col4:

    statuts_disponibles = sorted(
        [
            s for s in df_affiches["statut_libelle"].unique()
            if s and s != "nan"
        ]
    )

    statut_selectionne = st.selectbox(
        "Statut",
        ["Tous"] + statuts_disponibles
    )

with col5:

    recherche = st.text_input(
        "Rechercher",
        placeholder="Titre d'un film, d'une série ou d'un animé..."
    )


# ==========================
# APPLICATION DES FILTRES
# ==========================

df_filtre = df_affiches.copy()

# Filtre par type
if type_selectionne != "Tous":

    df_filtre = df_filtre[
        df_filtre["type_affichage"] == type_selectionne
    ]

# Filtre par statut
if statut_selectionne != "Tous":

    df_filtre = df_filtre[
        df_filtre["statut_libelle"] == statut_selectionne
    ]

# Recherche par titre
if recherche.strip():

    masque = df_filtre["title"].str.contains(
        recherche.strip(),
        case=False,
        na=False,
        regex=False
    )

    df_filtre = df_filtre[masque]


# ==========================
# APPLICATION DU TRI
# ==========================

ascending = ordre_tri == "Croissant"

if critere_tri == "Date de visionnage":

    df_filtre = df_filtre.sort_values(
        "date_affichage",
        ascending=ascending,
        na_position="last"
    )

elif critere_tri == "Titre":

    df_filtre = df_filtre.sort_values(
        "title",
        ascending=ascending,
        na_position="last",
        key=lambda s: s.str.lower()
    )

elif critere_tri == "Note":

    df_filtre = df_filtre.sort_values(
        "note_affichage",
        ascending=ascending,
        na_position="last"
    )


# ==========================
# NOMBRE DE RÉSULTATS
# ==========================

st.caption(
    f"{len(df_filtre)} élément(s) affiché(s) "
    f"sur {len(df_affiches)} au total"
)

st.divider()


# ==========================
# GRILLE RESPONSIVE DES AFFICHES
# ==========================

cartes_html = ""

for _, element in df_filtre.iterrows():

    # --------------------------
    # AFFICHE
    # --------------------------

    poster_path = element.get("poster_path", "")

    if pd.notna(poster_path) and str(poster_path).strip():

        poster_path = str(poster_path).strip()

        # URL complète ou chemin TMDB
        if poster_path.startswith(("https://", "http://")):

            poster_url = poster_path

        else:

            poster_url = (
                "https://image.tmdb.org/t/p/w500"
                + (
                    poster_path
                    if poster_path.startswith("/")
                    else "/" + poster_path
                )
            )

        affiche_html = f"""
            <img
                src="{html.escape(poster_url, quote=True)}"
                class="poster"
                loading="lazy"
            >
        """

    else:

        affiche_html = """
            <div class="pas-affiche">
                🎞️ Pas d'affiche
            </div>
        """

    # --------------------------
    # TITRE
    # --------------------------

    titre = html.escape(
        str(element.get("title", "Sans titre"))
    )

    # --------------------------
    # DATE
    # --------------------------

    date_vue = element.get("date_affichage")

    if pd.notna(date_vue):

        date_affichee = pd.Timestamp(
            date_vue
        ).strftime("%d/%m/%Y")

    else:

        date_affichee = "Non visionné"

    # --------------------------
    # NOTE
    # --------------------------

    note = element.get("note_affichage")

    if pd.notna(note) and str(note).strip():

        try:
            note_affichee = f"⭐ {float(note):g}/5"
        except (ValueError, TypeError):
            note_affichee = ""

    else:

        note_affichee = ""

    informations = html.escape(
        date_affichee
        + (f"  {note_affichee}" if note_affichee else "")
    )

    # --------------------------
    # CARTE COMPLÈTE
    # --------------------------

    cartes_html += f"""
        <div class="carte">
            {affiche_html}

            <div class="titre">
                {titre}
            </div>

            <div class="informations">
                {informations}
            </div>
        </div>
    """


# ==========================
# HTML ET CSS RESPONSIVES
# ==========================

html_page = f"""
<!DOCTYPE html>
<html>
<head>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

* {{
    box-sizing: border-box;
}}

html, body {{
    margin: 0;
    padding: 0;
    background: transparent;
    font-family: sans-serif;
}}

.grille {{
    display: grid;
    grid-template-columns: repeat(8, minmax(0, 1fr));
    gap: 18px 12px;
    width: 100%;
}}

.carte {{
    min-width: 0;
    text-align: center;
    overflow: hidden;
}}

.poster {{
    display: block;
    width: 100%;
    aspect-ratio: 2 / 3;
    object-fit: cover;
    border-radius: 8px;
}}

.pas-affiche {{
    width: 100%;
    aspect-ratio: 2 / 3;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background-color: rgba(128,128,128,0.12);
    border-radius: 8px;
    color: gray;
    font-size: 13px;
    padding: 5px;
}}

.titre {{
    color: white;
    text-align: center;
    font-size: 13px;
    font-weight: 600;
    line-height: 1.2;
    margin-top: 4px;
    overflow-wrap: anywhere;
}}

.informations {{
    color: white;
    opacity: 0.75;
    text-align: center;
    font-size: 11px;
    line-height: 1.2;
    margin-top: 3px;
    overflow-wrap: anywhere;
}}

/* Tablette */
@media (max-width: 900px) {{
    .grille {{
        grid-template-columns: repeat(4, minmax(0, 1fr));
    }}
}}

/* Téléphone : 3 affiches par ligne */
@media (max-width: 600px) {{
    .grille {{
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 16px 8px;
    }}

    .titre {{
        font-size: 12px;
    }}

    .informations {{
        font-size: 10px;
    }}
}}

</style>

</head>

<body>

<div class="grille">
    {cartes_html}
</div>

</body>
</html>
"""


# ==========================
# AFFICHAGE
# ==========================

# Estimation de la hauteur de la grille
nb_elements = len(df_filtre)

if nb_elements > 0:

    nb_lignes = (nb_elements + 7) // 8

    hauteur = max(
        100,
        nb_lignes * 250
    )

else:

    hauteur = 100
    st.info("Aucun élément ne correspond à ces filtres.")


components.html(
    html_page,
    height=hauteur,
    scrolling=False
)
