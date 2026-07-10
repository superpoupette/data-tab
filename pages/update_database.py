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


import streamlit as st

from scripts.importation_2024 import prepare_2024
from scripts.importation_2025 import prepare_2025
from scripts.danse.gestion_danses import (
    create_danse_data,
    create_danse_recap
)
from scripts.danse.google_sheet import save_danse_google_sheet

st.title("Dashboard Danse")

# ====================================
# Mise à jour de la base Google Sheet
# ====================================

if st.button("🔄 Mettre à jour la base de danse"):

    with st.spinner("Mise à jour..."):

        data2024 = prepare_2024("data/2024.csv")
        data2025 = prepare_2025("data/2025.csv")

        danse_2024 = create_danse_data(data2024)
        danse_2025 = create_danse_data(data2025)

        danse_data = pd.concat(
            [danse_2024, danse_2025],
            ignore_index=True
        )

        danse_recap = create_danse_recap(danse_data)

        save_danse_google_sheet(danse_recap)

    st.success("✅ Google Sheet mis à jour.")