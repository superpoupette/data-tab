import streamlit as st
import pandas as pd
import html

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

    # Harmonisation du format
    movies["date_affichage"] = movies["watched_at"]

    series_all["date_affichage"] = series_all["last_watch"]

    # Colonnes communes pour l'affichage
    movies["note_affichage"] = movies["rating"]
    series_all["note_affichage"] = pd.NA

    movies["statut_affichage"] = movies["status"]
    series_all["statut_affichage"] = series_all["status"]

    # Fusion des films, séries et animés
    df = pd.concat(
        [movies, series_all],
        ignore_index=True,
        sort=False
    )

    # Noms lisibles des types
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

    # Conversion des statuts en libellés
    statuts = {
        "watched": "Vu",
        "to_watch": "À voir",
        "continuing": "En cours",
        "up_to_date": "Terminé / à jour",
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
# FILTRES
# ==========================

col1, col2, col3, col4, col5 = st.columns(
    [1, 1.2, 1.2, 1.3, 2]
)

with col1:

    type_selectionne = st.selectbox(
        "Type",
        [
            "Tous",
            "Film",
            "Série",
            "Animé"
        ]
    )

with col2:

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

with col3:

    styles_disponibles = sorted(
        {
            style.strip()
            for valeur in df_affiches["style"].dropna()
            for style in str(valeur).split(",")
            if style.strip()
        }
    )

    style_selectionne = st.selectbox(
        "Style",
        ["Tous"] + styles_disponibles
    )

with col4:

    criteres_tri = [
        "Date de visionnage",
        "Titre",
        "Note"
    ]

    critere_tri = st.selectbox(
        "Trier par",
        criteres_tri
    )

with col5:

    recherche = st.text_input(
        "Rechercher",
        placeholder="Titre d'un film, d'une série ou d'un animé..."
    )


# ==========================
# FILTRES AVANCÉS
# ==========================

with st.expander("⚙️ Filtres supplémentaires"):

    col_a, col_b = st.columns(2)

    with col_a:

        ordre_tri = st.selectbox(
            "Ordre de tri",
            [
                "Décroissant",
                "Croissant"
            ]
        )

    with col_b:

        afficher_sans_affiche = st.checkbox(
            "Afficher uniquement les éléments sans affiche",
            value=False
        )


# ==========================
# APPLICATION DES FILTRES
# ==========================

df_filtre = df_affiches.copy()

# Type
if type_selectionne != "Tous":

    df_filtre = df_filtre[
        df_filtre["type_affichage"] == type_selectionne
    ]

# Statut
if statut_selectionne != "Tous":

    df_filtre = df_filtre[
        df_filtre["statut_libelle"] == statut_selectionne
    ]

# Style
if style_selectionne != "Tous":

    df_filtre = df_filtre[
        df_filtre["style"]
        .str.split(",")
        .apply(
            lambda styles: any(
                s.strip() == style_selectionne
                for s in styles
            )
        )
    ]

# Recherche
if recherche.strip():

    masque = df_filtre["title"].str.contains(
        recherche.strip(),
        case=False,
        na=False,
        regex=False
    )

    df_filtre = df_filtre[masque]

# Affiches manquantes
if afficher_sans_affiche:

    df_filtre = df_filtre[
        df_filtre["poster_path"].eq("")
        | df_filtre["poster_path"].isna()
    ]


# ==========================
# TRI
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
# RÉSULTATS
# ==========================

st.caption(
    f"{len(df_filtre)} élément(s) affiché(s) "
    f"sur {len(df_affiches)} au total"
)

st.divider()


# ==========================
# GRILLE DES AFFICHES
# ==========================

NB_COLONNES = 6

for i in range(0, len(df_filtre), NB_COLONNES):

    elements_ligne = df_filtre.iloc[
        i:i + NB_COLONNES
    ]

    colonnes = st.columns(NB_COLONNES)

    for col, (_, element) in zip(
        colonnes,
        elements_ligne.iterrows()
    ):

        with col:

            # --------------------------
            # AFFICHAGE DE L'AFFICHE
            # --------------------------

            poster_path = element.get("poster_path", "")

            if pd.notna(poster_path) and str(poster_path).strip():

                poster_path = str(poster_path).strip()

                # Accepte un chemin TMDB ou une URL complète
                if poster_path.startswith("https://") or poster_path.startswith("http://"):

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

                st.image(
                    poster_url,
                    use_container_width=True
                )

            else:

                st.markdown(
                    """
                    <div style="
                        width:100%;
                        aspect-ratio:2/3;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        text-align:center;
                        background-color:rgba(128,128,128,0.12);
                        border-radius:8px;
                        color:gray;
                    ">
                        🎞️<br>Pas d'affiche
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # --------------------------
            # TITRE
            # --------------------------

            titre = html.escape(
                str(element.get("title", "Sans titre"))
            )

            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    font-size:14px;
                    font-weight:600;
                    min-height:42px;
                    padding-top:6px;
                    overflow-wrap:anywhere;
                ">
                    {titre}
                </div>
                """,
                unsafe_allow_html=True
            )

            # --------------------------
            # TYPE ET STATUT
            # --------------------------

            type_label = html.escape(
                str(element.get("type_affichage", "Autre"))
            )

            statut_label = html.escape(
                str(element.get("statut_libelle", ""))
            )

            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    font-size:12px;
                    color:gray;
                    min-height:34px;
                ">
                    {type_label}<br>
                    {statut_label}
                </div>
                """,
                unsafe_allow_html=True
            )

            # --------------------------
            # NOTE
            # --------------------------

            note = element.get("note_affichage")

            if pd.notna(note) and str(note).strip():

                try:
                    note_affichee = f"⭐ {float(note):g}/10"
                except (ValueError, TypeError):
                    note_affichee = ""

                if note_affichee:
                    st.markdown(
                        f"""
                        <div style="
                            text-align:center;
                            font-size:13px;
                        ">
                            {note_affichee}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            # --------------------------
            # DATE
            # --------------------------

            date_vue = element.get("date_affichage")

            if pd.notna(date_vue):

                date_affichee = pd.Timestamp(
                    date_vue
                ).strftime("%d/%m/%Y")

                st.markdown(
                    f"""
                    <div style="
                        text-align:center;
                        font-size:12px;
                        color:gray;
                        padding-top:4px;
                    ">
                        {date_affichee}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.write("")
