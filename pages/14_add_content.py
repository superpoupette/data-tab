import streamlit as st
import pandas as pd

from scripts.watchlist.google_sheet import (
    add_movie_google_sheet,
    add_documentary_google_sheet,
    add_series_google_sheet,
    load_google_sheet,
    update_series_google_sheet,
    save_google_sheet
)

from scripts.watchlist.tmdb import (
    search_movies_tmdb,
    get_movie_details_tmdb,
    search_documentaries_tmdb,
    search_series_tmdb,
    get_series_details_tmdb
)

from scripts.musique.spotify_api import (
    enrichir_album_depuis_url
)

from scripts.musique.google_sheet import (
    ajouter_album_google_sheet
)

from scripts.danse.google_sheet import (
    add_danse_google_sheet,
    load_danse_google_sheet,
    add_practice_time
)


# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Ajouter du contenu",
    page_icon="💾",
    layout="wide"
)

NOTES = [i / 2 for i in range(11)]

STATUTS = [
    "continuing",
    "up_to_date",
    "stopped",
    "to_watch"
]

STYLES_DANSE = [
    "Urban",
    "Kpop girl",
    "Kpop boy",
    "Jazz",
    "Lyrical",
    "Street Jazz",
    "Dancehall",
    "Waacking/voguing",
    "Heels"
]


# =====================================================
# FONCTIONS UTILITAIRES
# =====================================================

def afficher_resultats(results, label, key):
    """Affiche les résultats TMDB et retourne le contenu choisi."""

    if not results:
        st.warning("Aucun résultat trouvé.")
        return None

    choix = st.selectbox(
        label,
        options=list(range(len(results))),
        format_func=lambda i: (
            f"{results[i]['title']} ({results[i]['year']})"
        ),
        key=key
    )

    selected = results[choix]

    col1, col2 = st.columns([1, 3])

    with col1:
        if selected.get("poster_path"):
            st.image(
                selected["poster_path"],
                use_container_width=True
            )

    with col2:
        st.subheader(selected["title"])
        st.caption(selected["year"])
        st.write(selected.get("overview", ""))

    st.divider()

    return selected


def charger_series():
    """Charge les séries depuis Google Sheets."""

    df = load_google_sheet("series")

    if not df.empty:
        df["progress"] = pd.to_numeric(
            df["progress"],
            errors="coerce"
        ).fillna(0)

        df["episodes"] = pd.to_numeric(
            df["episodes"],
            errors="coerce"
        ).fillna(0)

    return df


def recuperer_note(serie):
    """Retourne une note compatible avec le slider."""

    note = pd.to_numeric(
        serie.get("rating"),
        errors="coerce"
    )

    if pd.isna(note):
        return 0

    note = float(note)

    return note if note in NOTES else 0


# =====================================================
# MENU PRINCIPAL
# =====================================================

st.title("Ajouter du contenu")

type_contenu = st.selectbox(
    "Quel type de contenu souhaitez-vous gérer ?",
    [
        "Sélectionner un type de contenu",
        "Film",
        "Documentaire",
        "Série",
        "Album",
        "Danse"
    ],
    key="type_contenu"
)

st.divider()


# =====================================================
# FILM
# =====================================================

if type_contenu == "Film":

    st.header("🎬 Ajouter un film")

    movie_query = st.text_input(
        "Rechercher un film",
        placeholder="Ex : Interstellar",
        key="movie_query"
    )

    if st.button("🔎 Rechercher", key="search_movie"):
        if movie_query.strip():
            st.session_state["movie_results"] = (
                search_movies_tmdb(movie_query)
            )
        else:
            st.warning("Saisissez un titre.")

    if "movie_results" in st.session_state:

        selected = afficher_resultats(
            st.session_state["movie_results"],
            "Choisir le film",
            "movie_select"
        )

        if selected:

            col1, col2 = st.columns(2)

            with col1:
                movie_date = st.date_input(
                    "Date de visionnage",
                    key="movie_date"
                )

            with col2:
                movie_rating = st.select_slider(
                    "Ma note",
                    options=NOTES,
                    value=3,
                    key="movie_rating"
                )

            if st.button(
                "🎬 Ajouter le film",
                key="add_movie",
                use_container_width=True
            ):
                movie = get_movie_details_tmdb(
                    selected["id"]
                )

                add_movie_google_sheet(
                    movie,
                    movie_date.strftime("%Y-%m-%d"),
                    movie_rating
                )

                st.session_state.pop("movie_results", None)
                st.success("Film ajouté !")


# =====================================================
# DOCUMENTAIRE
# =====================================================

elif type_contenu == "Documentaire":

    st.header("🎥 Ajouter un documentaire")

    mode_documentaire = st.radio(
        "Comment souhaitez-vous ajouter le documentaire ?",
        ["Rechercher dans TMDB", "Saisie manuelle"],
        horizontal=True,
        key="documentary_mode"
    )

    # -------------------------------------------------
    # Recherche TMDB
    # -------------------------------------------------

    if mode_documentaire == "Rechercher dans TMDB":

        documentary_query = st.text_input(
            "Rechercher un documentaire",
            placeholder="Ex : Planète Terre",
            key="documentary_query"
        )

        if st.button(
            "🔎 Rechercher",
            key="search_documentary"
        ):
            if documentary_query.strip():
                st.session_state["documentary_results"] = (
                    search_documentaries_tmdb(documentary_query)
                )
            else:
                st.warning("Saisissez un titre.")

        if "documentary_results" in st.session_state:

            selected = afficher_resultats(
                st.session_state["documentary_results"],
                "Choisir le documentaire",
                "documentary_select"
            )

            if selected:

                col1, col2 = st.columns(2)

                with col1:
                    documentary_date = st.date_input(
                        "Date de visionnage",
                        key="documentary_date"
                    )

                    documentary_theme = st.text_input(
                        "Thème",
                        key="documentary_theme"
                    )

                with col2:
                    documentary_rating = st.select_slider(
                        "Ma note",
                        options=NOTES,
                        value=3,
                        key="documentary_rating"
                    )

                    documentary_platform = st.text_input(
                        "Plateforme",
                        key="documentary_platform"
                    )

                if st.button(
                    "🎥 Ajouter le documentaire",
                    key="add_documentary",
                    use_container_width=True
                ):
                    documentary = get_movie_details_tmdb(
                        selected["id"]
                    )

                    documentary["theme"] = documentary_theme
                    documentary["platform"] = documentary_platform

                    add_documentary_google_sheet(
                        documentary,
                        documentary_date.strftime("%Y-%m-%d"),
                        documentary_rating
                    )

                    st.session_state.pop(
                        "documentary_results", None
                    )

                    st.success("Documentaire ajouté !")

    # -------------------------------------------------
    # Saisie manuelle
    # -------------------------------------------------

    else:

        st.subheader("Informations du documentaire")

        with st.form("manual_documentary_form"):

            documentary_title = st.text_input("Titre *")

            col1, col2 = st.columns(2)

            with col1:
                documentary_year = st.text_input(
                    "Année",
                    placeholder="Ex : 2024"
                )

                documentary_date = st.date_input(
                    "Date de visionnage"
                )

                documentary_theme = st.text_input("Thème")

            with col2:
                documentary_rating = st.select_slider(
                    "Ma note",
                    options=NOTES,
                    value=3
                )

                documentary_platform = st.text_input(
                    "Plateforme"
                )

            documentary_director = st.text_input("Réalisateur")
            documentary_country = st.text_input("Pays")
            documentary_overview = st.text_area("Synopsis")

            documentary_poster = st.text_input(
                "URL de l'affiche (facultatif)"
            )

            submitted = st.form_submit_button(
                "🎥 Ajouter le documentaire",
                use_container_width=True
            )

            if submitted:

                if not documentary_title.strip():
                    st.error("Le titre est obligatoire.")

                else:
                    documentary = {
                        "title": documentary_title,
                        "year": documentary_year,
                        "director": documentary_director,
                        "theme": documentary_theme,
                        "platform": documentary_platform,
                        "country": documentary_country,
                        "overview": documentary_overview,
                        "poster_path": documentary_poster,
                        "tmdb_rating": "",
                        "imdb_id": "",
                        "tvdb_id": ""
                    }

                    add_documentary_google_sheet(
                        documentary,
                        documentary_date.strftime("%Y-%m-%d"),
                        documentary_rating
                    )

                    st.success("Documentaire ajouté !")


# =====================================================
# SÉRIE
# =====================================================

elif type_contenu == "Série":

    st.header("📺 Gestion des séries")

    action_serie = st.radio(
        "Que souhaitez-vous faire ?",
        [
            "Ajouter une série",
            "Mettre à jour un épisode",
            "Modifier une série"
        ],
        key="action_serie"
    )

    st.divider()

    # -------------------------------------------------
    # Ajouter une série
    # -------------------------------------------------

    if action_serie == "Ajouter une série":

        query = st.text_input(
            "Rechercher une série",
            placeholder="Ex : Breaking Bad",
            key="series_query"
        )

        if st.button(
            "🔎 Rechercher",
            key="search_series"
        ):
            if query.strip():
                st.session_state["series_results"] = (
                    search_series_tmdb(query)
                )
            else:
                st.warning("Saisissez un titre.")

        if "series_results" in st.session_state:

            selected = afficher_resultats(
                st.session_state["series_results"],
                "Choisir la série",
                "series_select"
            )

            if selected:

                if st.button(
                    "📺 Ajouter la série",
                    key="add_series",
                    use_container_width=True
                ):
                    serie = get_series_details_tmdb(
                        selected["id"]
                    )

                    add_series_google_sheet(serie)

                    st.session_state.pop("series_results", None)
                    st.success("Série ajoutée !")

    # -------------------------------------------------
    # Mettre à jour un épisode
    # -------------------------------------------------

    elif action_serie == "Mettre à jour un épisode":

        st.subheader("Mettre à jour une série")

        series_df = charger_series()

        if series_df.empty:
            st.info("Aucune série disponible.")

        else:
            series_continuing = series_df[
                (series_df["type"] == "series")
                & (series_df["status"] == "continuing")
            ].copy()

            if series_continuing.empty:
                st.info("Aucune série en cours.")

            else:
                serie_index = st.selectbox(
                    "Choisir une série",
                    options=series_continuing.index.tolist(),
                    format_func=lambda i: (
                        series_continuing.loc[i, "title"]
                    ),
                    key="update_series_select"
                )

                serie = series_df.loc[serie_index]

                st.write(
                    f"Épisodes vus actuellement : "
                    f"{int(serie['progress'])}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    episode = st.number_input(
                        "Dernier épisode vu",
                        min_value=0,
                        value=int(serie["progress"]),
                        step=1,
                        key=f"episode_{serie_index}"
                    )

                with col2:
                    date_watch = st.date_input(
                        "Date du visionnage",
                        key="episode_date"
                    )

                current_status = serie["status"]

                statut = st.selectbox(
                    "Statut",
                    STATUTS,
                    index=(
                        STATUTS.index(current_status)
                        if current_status in STATUTS
                        else 0
                    ),
                    key=f"update_status_{serie_index}"
                )

                rating = st.select_slider(
                    "Ma note",
                    options=NOTES,
                    value=recuperer_note(serie),
                    key=f"update_rating_{serie_index}"
                )

                if st.button(
                    "💾 Mettre à jour la série",
                    key="update_series",
                    use_container_width=True
                ):
                    series_df.loc[
                        serie_index, "progress"
                    ] = int(episode)

                    series_df.loc[
                        serie_index, "last_watch"
                    ] = date_watch.strftime("%Y-%m-%d")

                    series_df.loc[
                        serie_index, "status"
                    ] = statut

                    series_df.loc[
                        serie_index, "rating"
                    ] = rating

                    update_series_google_sheet(series_df)

                    st.success("Série mise à jour !")

    # -------------------------------------------------
    # Modifier une série
    # -------------------------------------------------

    elif action_serie == "Modifier une série":

        st.subheader("✏️ Modifier une série")

        series_df = charger_series()

        if series_df.empty:
            st.info("Aucune série disponible.")

        else:
            search_serie = st.text_input(
                "🔎 Rechercher une série",
                placeholder="Ex : Breaking",
                key="edit_series_search"
            )

            filtered = series_df[
                series_df["title"].notna()
            ].copy()

            if search_serie.strip():
                filtered = filtered[
                    filtered["title"].str.contains(
                        search_serie.strip(),
                        case=False,
                        na=False,
                        regex=False
                    )
                ]

            filtered = filtered.sort_values("title")

            if not search_serie.strip():
                filtered = filtered.head(20)

            if filtered.empty:
                st.info("Aucune série correspondante.")

            else:
                serie_index = st.selectbox(
                    "Choisir une série",
                    options=filtered.index.tolist(),
                    format_func=lambda i: (
                        filtered.loc[i, "title"]
                    ),
                    key="edit_series_select"
                )

                serie = series_df.loc[serie_index]

                st.write(
                    f"Modification de : **{serie['title']}**"
                )

                col1, col2 = st.columns(2)

                with col1:
                    current_status = serie.get("status", "")

                    new_status = st.selectbox(
                        "Statut",
                        STATUTS,
                        index=(
                            STATUTS.index(current_status)
                            if current_status in STATUTS
                            else 0
                        ),
                        key=f"edit_status_{serie_index}"
                    )

                with col2:
                    new_rating = st.select_slider(
                        "Note",
                        options=NOTES,
                        value=recuperer_note(serie),
                        key=f"edit_rating_{serie_index}"
                    )

                if st.button(
                    "💾 Enregistrer les modifications",
                    key="save_series_edit",
                    use_container_width=True
                ):
                    series_df.loc[
                        serie_index, "status"
                    ] = new_status

                    series_df.loc[
                        serie_index, "rating"
                    ] = new_rating

                    save_google_sheet(series_df, "series")

                    st.success("Série modifiée !")


# =====================================================
# ALBUM
# =====================================================

elif type_contenu == "Album":

    st.header("💿 Ajouter un album")

    lien_spotify = st.text_input(
        "Lien Spotify de l'album",
        placeholder="https://open.spotify.com/album/...",
        key="spotify_url"
    )

    if st.button(
        "🔎 Charger l'album",
        key="load_album"
    ):
        if lien_spotify.strip():
            infos = enrichir_album_depuis_url(lien_spotify)
            st.session_state["album_infos"] = infos
        else:
            st.warning("Saisissez un lien Spotify.")

    if "album_infos" in st.session_state:

        infos = st.session_state["album_infos"]

        if infos:

            col1, col2 = st.columns([1, 3])

            with col1:
                if infos.get("cover_url"):
                    st.image(
                        infos["cover_url"],
                        use_container_width=True
                    )

            with col2:
                st.subheader(infos["spotify_album"])
                st.write(infos["spotify_artiste"])
                st.write(infos["spotify_date_sortie"])
                st.write(f"{infos['nb_titres']} titres")

            col1, col2 = st.columns(2)

            with col1:
                genre = st.selectbox(
                    "Genre",
                    [
                        "Pop",
                        "Rock",
                        "Rap",
                        "Kpop",
                        "Jpop",
                        "RnB",
                        "Indie",
                        "Electro/techno",
                        "Variété",
                        "Autre"
                    ],
                    key="album_genre"
                )

            with col2:
                pays = st.text_input(
                    "Pays",
                    placeholder="Ex : France, USA, Corée",
                    key="album_pays"
                )

            note = st.select_slider(
                "Note",
                options=list(range(11)),
                value=5,
                key="album_note"
            )

            date = st.date_input(
                "Date d'ajout",
                key="album_date"
            )

            if st.button(
                "Ajouter l'album",
                key="add_album",
                use_container_width=True
            ):
                infos["Date"] = date.strftime("%Y-%m-%d")
                infos["Genre (large)"] = genre
                infos["Pays"] = pays
                infos["Note"] = note

                ajouter_album_google_sheet(infos)

                st.session_state.pop("album_infos", None)

                st.success("Album ajouté !")


# =====================================================
# DANSE
# =====================================================

elif type_contenu == "Danse":

    st.header("💃 Gestion de la danse")

    action_danse = st.radio(
        "Que souhaitez-vous faire ?",
        [
            "Ajouter du temps de pratique",
            "Ajouter une chorégraphie"
        ],
        key="action_danse"
    )

    st.divider()

    # -------------------------------------------------
    # Ajouter du temps de pratique
    # -------------------------------------------------

    if action_danse == "Ajouter du temps de pratique":

        st.subheader("Chorégraphies en cours")

        danses = load_danse_google_sheet()

        if danses.empty:
            st.info("Aucune chorégraphie enregistrée.")

        else:
            danses_en_cours = danses[
                danses["statut"] == "en cours"
            ].copy()

            if danses_en_cours.empty:
                st.info("Aucune chorégraphie en cours.")

            else:
                danses_en_cours["label"] = (
                    danses_en_cours["artiste"].fillna("").astype(str)
                    + " - "
                    + danses_en_cours["titre"].fillna("").astype(str)
                )

                choix_index = st.selectbox(
                    "Chorégraphie travaillée",
                    options=danses_en_cours.index.tolist(),
                    format_func=lambda i: (
                        danses_en_cours.loc[i, "label"]
                    ),
                    key="danse_select"
                )

                ligne = danses_en_cours.loc[choix_index]

                duree_danse = st.number_input(
                    "Durée de pratique (min)",
                    min_value=0,
                    step=5,
                    key="danse_practice_duration"
                )

                if st.button(
                    "💃 Ajouter le temps de pratique",
                    key="add_danse_practice",
                    use_container_width=True
                ):
                    if duree_danse <= 0:
                        st.warning(
                            "La durée doit être supérieure à 0 minute."
                        )

                    else:
                        succes = add_practice_time(
                            ligne["artiste"],
                            ligne["titre"],
                            duree_danse
                        )

                        if succes:
                            st.success(
                                f"{duree_danse} minutes ajoutées à "
                                f"{ligne['artiste']} - {ligne['titre']} !"
                            )

                        else:
                            st.error(
                                "Impossible de trouver la chorégraphie."
                            )

    # -------------------------------------------------
    # Ajouter une chorégraphie
    # -------------------------------------------------

    elif action_danse == "Ajouter une chorégraphie":

        st.subheader("Nouvelle chorégraphie")

        with st.form("nouvelle_choregraphie_form"):

            col1, col2, col3 = st.columns(3)

            with col1:
                new_artiste = st.text_input(
                    "Artiste *",
                    key="new_artiste"
                )

            with col2:
                new_titre = st.text_input(
                    "Titre *",
                    key="new_titre"
                )

            with col3:
                new_choregraphe = st.text_input(
                    "Chorégraphe",
                    key="new_choregraphe"
                )

            col4, col5 = st.columns(2)

            with col4:
                new_style = st.selectbox(
                    "Style",
                    STYLES_DANSE,
                    key="new_style"
                )

            with col5:
                new_duree = st.number_input(
                    "Durée de la chorégraphie (s)",
                    min_value=0,
                    step=10,
                    key="new_duree"
                )

            submitted = st.form_submit_button(
                "➕ Ajouter la chorégraphie",
                use_container_width=True
            )

            if submitted:

                if not new_artiste.strip() or not new_titre.strip():
                    st.error(
                        "L'artiste et le titre sont obligatoires."
                    )

                else:
                    add_danse_google_sheet(
                        artiste=new_artiste.strip(),
                        titre=new_titre.strip(),
                        choregraphe=new_choregraphe.strip(),
                        style=new_style,
                        duree=new_duree
                    )

                    st.success("Chorégraphie ajoutée !")
