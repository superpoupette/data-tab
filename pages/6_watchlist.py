import streamlit as st
import pandas as pd
import plotly.express as px

from scripts.watchlist.load_watchlist import load_movies_google_sheet


# =====================
# Chargement données
# =====================

movies = load_movies_google_sheet()


st.title("🍿 Ma watchlist")


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

st.subheader("Films vus par mois")


movies_month = (
    movies[
        (movies["status"] == "watched")
        &
        (movies["watched_at"].notna())
        &
        (movies["watched_at"] >= "2023-01-01")
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
# STYLES + RATINGS
# =====================


col_style, col_rating = st.columns(2)



# =====================
# CAMEMBERT STYLES
# =====================

with col_style:

    st.subheader("Répartition des styles")


    styles = (
        movies[
            movies["status"] == "watched"
        ]
        ["style"]
        .dropna()
        .str.split(", ")
        .explode()
        .value_counts()
    )


    # Garder les 10 styles principaux
    top_styles = styles.head(10)


    # Regrouper le reste
    other = styles.iloc[10:].sum()


    if other > 0:
        top_styles.loc["Autre"] = other


    styles_df = (
        top_styles
        .reset_index()
    )


    styles_df.columns = [
        "style",
        "count"
    ]


    fig_style = px.pie(
        styles_df,
        names="style",
        values="count",
        hole=0
    )


    fig_style.update_layout(
        height=400,
        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        )
    )


    st.plotly_chart(
        fig_style,
        use_container_width=True
    )

# =====================
# REPARTITION RATINGS
# =====================

with col_rating:

    st.subheader("Répartition des notes")


    ratings = (
        movies[
            movies["status"] == "watched"
        ]
        ["rating"]
        .dropna()
        .value_counts()
        .sort_index()
        .reset_index()
    )


    ratings.columns = [
        "rating",
        "count"
    ]


    fig_rating = px.bar(
        ratings,
        x="rating",
        y="count",
        text="count"
    )


    fig_rating.update_layout(
        height=400,
        xaxis_title="Note",
        yaxis_title="Nombre de films",
        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        )
    )


    st.plotly_chart(
        fig_rating,
        use_container_width=True
    )


# =====================
# DERNIERS FILMS VUS
# =====================

st.subheader("Mes 6 derniers films vus")


last_6_movies = (
    movies[
        movies["status"] == "watched"
    ]
    .sort_values(
        "watched_at",
        ascending=False
    )
    .head(6)
)


cols = st.columns(6)


for col, (_, movie) in zip(
    cols,
    last_6_movies.iterrows()
):

    with col:

        # Titre au-dessus de l'affiche
        st.markdown(
            f"""
            <div style="
                text-align:center;
                font-size:14px;
                font-weight:600;
                height:45px;
            ">
                {movie["title"]}
            </div>
            """,
            unsafe_allow_html=True
        )


        # Affiche
        if pd.notna(movie.get("poster_path")):

            poster_url = (
                "https://image.tmdb.org/t/p/w500"
                + movie["poster_path"]
            )

            st.image(
                poster_url,
                use_container_width=True
            )

        else:

            st.write(
                "Pas d'affiche"
            )


        # Date sous l'affiche
        date_vue = movie["watched_at"].strftime("%d/%m/%Y")

        st.markdown(
            f"""
            <div style="
                text-align:center;
                font-size:13px;
                color:gray;
            ">
                Vu le {date_vue}
            </div>
            """,
            unsafe_allow_html=True
        )

from scripts.watchlist.update_watchlist import update_series

series = update_series()

st.header("📺 Séries")
st.dataframe(
    series,
    use_container_width=True
)