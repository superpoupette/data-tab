import streamlit as st

from scripts.watchlist.google_sheet import (
    add_movie_google_sheet,
    add_series_google_sheet
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

            serie["rating"] = rating

            add_series_google_sheet(
                serie
            )

            st.success(
                "Série ajoutée !"
            )