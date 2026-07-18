import streamlit as st
import pandas as pd

from scripts.watchlist.update_watchlist import (
    update_movies,
    update_series
)

from scripts.importation_2024 import prepare_2024
from scripts.importation_2025 import prepare_2025

from scripts.danse.gestion_danses import (
    create_danse_data,
    create_danse_recap
)

from scripts.danse.google_sheet import (
    save_danse_google_sheet
)


st.set_page_config(
    page_title="Update Database"
)

st.title("🔄 Mise à jour des bases de données")


# =====================================================
# WATCHLIST
# =====================================================

st.header("🍿 Watchlist")

st.write(
    "Met à jour les films et les séries depuis TV Time "
    "et les animes depuis MyAnimeList."
)


col1, col2 = st.columns(2)


# ===========================
# FILMS
# ===========================

with col1:

    if st.button("🎬 Mettre à jour les films"):

        with st.spinner("Mise à jour des films..."):

            try:

                movies = update_movies()

                st.success("Films mis à jour.")

                st.metric(
                    "Nombre de films",
                    len(movies)
                )

                st.dataframe(
                    movies.head(10),
                    use_container_width=True
                )

            except Exception as e:

                st.exception(e)


# ===========================
# SERIES
# ===========================

with col2:

    if st.button("📺 Mettre à jour les séries"):

        with st.spinner("Mise à jour des séries..."):

            try:

                series = update_series()

                st.success("Séries et animes mis à jour.")

                st.metric(
                    "Nombre de séries/animes",
                    len(series)
                )

                st.dataframe(
                    series.head(10),
                    use_container_width=True
                )

            except Exception as e:

                st.exception(e)


st.divider()


# =====================================================
# DANSE
# =====================================================

st.header("💃 Danse")

if st.button("🔄 Mettre à jour la base de danse"):

    with st.spinner("Mise à jour..."):

        data2024 = prepare_2024(
            "data/2024.csv"
        )

        data2025 = prepare_2025(
            "data/2025.csv"
        )

        danse_2024 = create_danse_data(
            data2024
        )

        danse_2025 = create_danse_data(
            data2025
        )

        danse_data = pd.concat(
            [
                danse_2024,
                danse_2025
            ],
            ignore_index=True
        )

        danse_recap = create_danse_recap(
            danse_data
        )

        save_danse_google_sheet(
            danse_recap
        )

    st.success(
        "Base danse mise à jour."
    )