import streamlit as st
import pandas as pd

from scripts.watchlist.google_sheet import (
    add_movie_google_sheet,
    add_series_google_sheet,
    load_google_sheet,
    update_series_google_sheet,
    save_google_sheet
)

from scripts.watchlist.tmdb import (
    search_movies_tmdb,
    get_movie_details_tmdb,
    search_series_tmdb,
    get_series_details_tmdb
)




st.set_page_config(
    page_title="Ajouter à la watchlist"
)


st.title("🎬 Ajouter un film")


movie_query = st.text_input(
    "Rechercher un film",
    placeholder="Ex : Interstellar",
    key="movie_query"
)

if st.button(
    "🔎 Rechercher",
    key="search_movie"
):

    st.session_state["movie_results"] = search_movies_tmdb(
        movie_query
    )

if "movie_results" in st.session_state:

    results = st.session_state["movie_results"]

    if len(results) > 0:

        choix = st.selectbox(
            "Choisir le film",
            [
                f"{movie['title']} ({movie['year']})"
                for movie in results
            ],
            key="movie_select"
        )

        selected = results[
            [
                f"{movie['title']} ({movie['year']})"
                for movie in results
            ].index(choix)
        ]

        col1, col2 = st.columns([1, 3])

        with col1:

            if selected["poster_path"]:

                st.image(
                    selected["poster_path"],
                    use_container_width=True
                )

        with col2:

            st.subheader(selected["title"])

            st.caption(selected["year"])

            st.write(
                selected["overview"]
            )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            movie_date = st.date_input(
                "Date de visionnage",
                key="movie_date"
            )
            

        with col2:

            movie_rating = st.select_slider(
                "Ma note",
                options=[
                    0,
                    0.5,
                    1,
                    1.5,
                    2,
                    2.5,
                    3,
                    3.5,
                    4,
                    4.5,
                    5
                ],
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

            st.success("Film ajouté !")

    else:

        st.warning(
            "Aucun film trouvé."
        )





st.title("📺 Ajouter une série")

query = st.text_input(
    "Rechercher une série",
    placeholder="Ex : Breaking Bad",
    key="series_query"
)

if st.button(
    "🔎 Rechercher",
    key="search_series"
):

    st.session_state["series_results"] = (
        search_series_tmdb(query)
    )

if "series_results" in st.session_state:

    results = st.session_state["series_results"]

    if results:

        choix = st.selectbox(
            "Choisir la série",
            [
                f"{s['title']} ({s['year']})"
                for s in results
            ],
            key="series_select"
        )

        selected = results[
            [
                f"{s['title']} ({s['year']})"
                for s in results
            ].index(choix)
        ]

        col1, col2 = st.columns([1,3])

        with col1:

            if selected["poster_path"]:

                st.image(
                    selected["poster_path"],
                    use_container_width=True
                )

        with col2:

            st.subheader(
                selected["title"]
            )

            st.caption(
                selected["year"]
            )

            st.write(
                selected["overview"]
            )

        st.divider()

        if st.button(
            "📺 Ajouter la série",
            key="add_series",
            use_container_width=True
        ):

            serie = get_series_details_tmdb(
                selected["id"]
            )

            add_series_google_sheet(
                serie
            )

            st.success(
                "Série ajoutée !"
            )



# =====================================================
# Ajouter un épisode vu sur une série existante
# =====================================================

st.divider()

st.title("📺 Mise à jour d'une série")


series_df = load_google_sheet(
    "series"
)


series_df["progress"] = pd.to_numeric(
    series_df["progress"],
    errors="coerce"
).fillna(0)

series_df["episodes"] = pd.to_numeric(
    series_df["episodes"],
    errors="coerce"
).fillna(0)

# uniquement séries TV en cours

series_continuing = series_df[
    (series_df["type"] == "series")
    &
    (series_df["status"] == "continuing")
].copy()



if len(series_continuing) == 0:

    st.info(
        "Aucune série en cours."
    )


else:


    choix = st.selectbox(
        "Choisir une série",
        series_continuing["title"].tolist(),
        key="update_series_select"
    )


    serie_index = series_continuing[
        series_continuing["title"] == choix
    ].index[0]


    serie = series_df.loc[
        serie_index
    ]


    st.write(
        f"Épisodes vus actuellement : {serie['progress']}"
    )


    col1, col2 = st.columns(2)


    with col1:

        episode = st.number_input(
            "Dernier épisode vu",
            min_value=0,
            value=int(
                serie["progress"]
                if pd.notna(serie["progress"])
                else 0
            ),
            step=1
        )


    with col2:

        date_watch = st.date_input(
            "Date du visionnage",
            key="episode_date"
        )


    statut = st.selectbox(
        "Statut",
        [
            "continuing",
            "up_to_date",
            "stopped",
            "watch_later"
        ],
        index=[
            "continuing",
            "up_to_date",
            "stopped",
            "watch_later"
        ].index(
            serie["status"]
        )
        if serie["status"] in [
            "continuing",
            "up_to_date",
            "stopped",
            "watch_later"
        ]
        else 0
    )


    ancienne_note = pd.to_numeric(
        serie.get("rating"),
        errors="coerce"
    )

    if pd.isna(ancienne_note):
        ancienne_note = 0


    rating = st.select_slider(
        "Ma note",
        options=[
            0,
            0.5,
            1,
            1.5,
            2,
            2.5,
            3,
            3.5,
            4,
            4.5,
            5
        ],
        value=float(
            ancienne_note
        )
    )



    if st.button(
        "💾 Mettre à jour la série",
        use_container_width=True
    ):


        series_df.loc[
            serie_index,
            "progress"
        ] = int(episode)


        series_df.loc[
            serie_index,
            "last_watch"
        ] = date_watch.strftime(
            "%Y-%m-%d"
        )


        series_df.loc[
            serie_index,
            "status"
        ] = statut

        series_df["rating"] = pd.to_numeric(
            series_df["rating"],
            errors="coerce"
        )

        series_df.loc[
            serie_index,
            "rating"
        ] = rating


        
        update_series_google_sheet(
            series_df
        )


        st.success(
            "Série mise à jour !"
        )

        st.rerun()


# =====================================================
# MODIFIER UNE SERIE
# =====================================================

st.divider()

st.header("✏️ Modifier une série")


series_df = load_google_sheet(
    "series"
)


if not series_df.empty:


    # Sélection uniquement séries/animes existants
    serie_choices = (
        series_df["title"]
        .dropna()
        .tolist()
    )


    selected_title = st.selectbox(
        "Choisir une série",
        serie_choices,
        key="edit_series_select"
    )


    serie_index = series_df[
        series_df["title"] == selected_title
    ].index[0]


    serie = series_df.loc[
        serie_index
    ]


    st.write(
        f"Modification de : **{serie['title']}**"
    )


    col1, col2 = st.columns(2)


    with col1:

        current_status = serie.get(
            "status",
            ""
        )

        statuses = [
            "continuing",
            "up_to_date",
            "to_watch",
            "stopped"
        ]


        new_status = st.selectbox(
            "Statut",
            statuses,
            index=(
                statuses.index(current_status)
                if current_status in statuses
                else 0
            ),
            key="edit_status"
        )


    with col2:

        current_rating = serie.get(
            "rating",
            0
        )


        if pd.isna(current_rating):
            current_rating = 0


        new_rating = st.select_slider(
            "Note",
            options=[
                0,
                0.5,
                1,
                1.5,
                2,
                2.5,
                3,
                3.5,
                4,
                4.5,
                5
            ],
            value=float(current_rating),
            key="edit_rating"
        )


    if st.button(
        "💾 Enregistrer les modifications",
        use_container_width=True,
        key="save_series_edit"
    ):


        series_df.loc[
            serie_index,
            "status"
        ] = new_status


        series_df.loc[
            serie_index,
            "rating"
        ] = new_rating


        # sauvegarde
        save_google_sheet(
            series_df,
            "series"
        )


        st.success(
            "Série modifiée !"
        )

        st.rerun()

else:

    st.info(
        "Aucune série disponible."
    )