import streamlit as st
import pandas as pd

from scripts.watchlist.load_watchlist import load_movies_google_sheet


# =====================
# Chargement données
# =====================

movies = load_movies_google_sheet()


st.title("🍿 Watchlist Films")


# =====================
# FILMS
# =====================

st.header("🎬 Films")


with st.container():

    nb_movies_watched = (
        movies["status"] == "watched"
    ).sum()


    nb_movies_to_watch = (
        movies["status"] == "to_watch"
    ).sum()


    watched_movies = (
        movies[
            movies["status"] == "watched"
        ]
        .sort_values(
            "watched_at",
            ascending=False
        )
    )


    if len(watched_movies) > 0:
        last_movie = watched_movies.iloc[0]["title"]
    else:
        last_movie = "Aucun film vu"


    col1, col2, col3 = st.columns(3)


    with col1:
        st.metric(
            "Films vus",
            nb_movies_watched
        )


    with col2:
        st.metric(
            "Films à voir",
            nb_movies_to_watch
        )


    with col3:

        st.markdown(
            f"""
            <div style="font-size:14px;">
                Dernier film vu
            </div>

            <div style="font-size:22px;font-weight:600;">
                {last_movie}
            </div>
            """,
            unsafe_allow_html=True
        )



# =====================
# FILMS VUS PAR MOIS
# =====================

st.subheader("📈 Films vus par mois")


movies_month = (
    movies[
        (movies["status"] == "watched")
        &
        (movies["watched_at"].notna())
    ]
    .assign(
        month=lambda x:
        x["watched_at"]
        .dt.to_period("M")
        .astype(str)
    )
    .groupby("month")
    .size()
)


st.line_chart(
    movies_month
)



# =====================
# GENRES
# =====================

st.subheader("🎭 Genres vus")


genres = (
    movies[
        movies["status"] == "watched"
    ]
    ["style"]
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
)


st.bar_chart(
    genres
)



# =====================
# DERNIERS VISIONNAGES
# =====================

st.header("📌 Derniers visionnages")


last_seen = (
    movies[
        movies["status"] == "watched"
    ]
    [
        [
            "title",
            "style",
            "watched_at",
            "rating",
            "tmdb_rating"
        ]
    ]
    .sort_values(
        "watched_at",
        ascending=False
    )
)


st.dataframe(
    last_seen,
    use_container_width=True,
    hide_index=True
)



# =====================
# BASE COMPLETE
# =====================

st.header("🎞️ Base films")


st.dataframe(
    movies,
    use_container_width=True,
    hide_index=True
)