import streamlit as st

from scripts.watchlist.update_watchlist import update_movies


st.set_page_config(
    page_title="Update Database"
)


st.title("🔄 Mise à jour base de données")


st.write(
    "Cette page récupère les données TV Time, "
    "ajoute les informations TMDB et met à jour Google Sheet."
)



if st.button("🚀 Mettre à jour les films"):

    with st.spinner("Mise à jour en cours..."):

        try:

            movies = update_movies()


            st.success(
                "Base mise à jour avec succès !"
            )


            st.metric(
                "Nombre de films",
                len(movies)
            )


            st.subheader(
                "Aperçu"
            )


            st.dataframe(
                movies.head(10),
                use_container_width=True
            )


        except Exception as e:

            st.error(
                "Une erreur est survenue :"
            )

            st.exception(e)