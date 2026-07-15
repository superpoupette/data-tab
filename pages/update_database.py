import streamlit as st

from scripts.watchlist.update_watchlist import (
    add_movie_google_sheet
)

from scripts.watchlist.tmdb import (
    search_movies_tmdb,
    get_movie_details_tmdb
)


st.set_page_config(
    page_title="Watchlist"
)


st.title("🎬 Ajouter un film")


# =====================
# Recherche TMDB
# =====================

st.subheader("Recherche d'un film")


movie_query = st.text_input(
    "Nom du film",
    placeholder="Ex : Interstellar"
)


if st.button(
    "🔎 Rechercher",
    key="search_movie"
):

    if movie_query.strip():

        results = search_movies_tmdb(
            movie_query
        )

        st.session_state["movie_results"] = results

    else:

        st.warning(
            "Veuillez entrer un nom de film."
        )



# =====================
# Résultats recherche
# =====================

if "movie_results" in st.session_state:


    results = st.session_state["movie_results"]


    if len(results) > 0:


        choix = st.selectbox(
            "Choisir le film",
            [
                f"{m['title']} ({m['year']})"
                for m in results
            ],
            key="movie_choice"
        )


        index = [
            f"{m['title']} ({m['year']})"
            for m in results
        ].index(
            choix
        )


        selected = results[index]



        col1, col2 = st.columns(
            [1, 3]
        )


        with col1:

            if selected["poster_path"]:

                st.image(
                    selected["poster_path"],
                    width=150
                )



        with col2:

            st.subheader(
                selected["title"]
            )

            if selected["year"]:

                st.write(
                    f"📅 Année : {selected['year']}"
                )


            if selected["overview"]:

                st.write(
                    selected["overview"]
                )



        st.divider()



        # =====================
        # Informations utilisateur
        # =====================


        movie_date = st.date_input(
            "Date de visionnage",
            key="movie_date"
        )


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
            key="movie_rating"
        )



        # =====================
        # Ajout Google Sheet
        # =====================


        if st.button(
            "🎬 Ajouter ce film",
            key="add_movie"
        ):


            try:

                movie = get_movie_details_tmdb(
                    selected["id"]
                )


                add_movie_google_sheet(
                    movie,
                    movie_date.strftime(
                        "%Y-%m-%d"
                    ),
                    movie_rating
                )


                st.success(
                    f"{movie['title']} ajouté à la watchlist !"
                )


                # nettoyage recherche
                del st.session_state["movie_results"]


            except Exception as e:

                st.error(
                    f"Erreur lors de l'ajout : {e}"
                )



    else:

        st.info(
            "Aucun résultat trouvé."
        )