import streamlit as st
import pandas as pd
import plotly.express as px

from scripts.watchlist.load_watchlist import (
    load_movies_google_sheet,
    load_series_google_sheet
)

st.set_page_config(
    page_title="Watchlist",
    page_icon="🍿",
    layout="wide"
)

# =====================
# Chargement données
# =====================

movies = load_movies_google_sheet()
series_all = load_series_google_sheet()


# Nettoyage type
series_all["type"] = (
    series_all["type"]
    .astype(str)
    .str.strip()
    .str.lower()
)


series = series_all[
    series_all["type"] == "series"
].copy()


animes = series_all[
    series_all["type"] == "anime"
].copy()

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
st.write("")
# =====================
# DERNIERS FILMS VUS
# =====================

st.subheader("Derniers films vus")


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

st.write("")
st.write("")

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
# CAMEMBERT PAYS D'ORIGINE
# =====================

st.subheader("Pays d'origine des films")

countries = (
    movies[movies["status"] == "watched"]["country"]
    .dropna()
    .str.split(", ")
    .explode()
    .str.strip()
)

countries = countries.value_counts()

# Regrouper les pays < 1 % dans "Autres"
countries_df = countries.reset_index()
countries_df.columns = ["country", "count"]

total = countries_df["count"].sum()
countries_df["pct"] = countries_df["count"] / total * 100

main = countries_df[countries_df["pct"] >= 1].copy()
others = countries_df[countries_df["pct"] < 1]["count"].sum()

if others > 0:
    main = pd.concat(
        [
            main,
            pd.DataFrame([{
                "country": "Autres",
                "count": others
            }])
        ],
        ignore_index=True
    )

fig_country = px.pie(
    main,
    names="country",
    values="count"
)

fig_country.update_layout(
    height=450,
    margin=dict(l=0, r=0, t=30, b=0)
)

st.plotly_chart(fig_country, use_container_width=True)

st.write("")
st.write("")
st.write("")

# =====================
# Cartes Anime / Séries
# =====================

st.header("📺 Épisodes")

col_series, col_animes = st.columns(2)


# =====================
# Séries
# =====================

with col_series:

    with st.container(border=True):

        st.subheader("Séries")

        total_series = len(series)

        finished = (
            series["status"] == "up_to_date"
        ).sum()

        watching = (
            series["status"] == "continuing"
        ).sum()

        to_watch = (
            series["status"] == "to_watch"
        ).sum()

        stopped = (
            series["status"] == "stopped"
        ).sum()

        total_series_episodes_watched = (
            series["progress"]
            .fillna(0)
            .sum()
        )


        stats_series = pd.DataFrame(
            {
                "Statut": [
                    "Terminées",
                    "En cours",
                    "À voir",
                    "Stoppées"
                ],
                "Nombre": [
                    finished,
                    watching,
                    to_watch,
                    stopped
                ]
            }
        )


        stats_series["Pourcentage"] = (
            stats_series["Nombre"]
            /
            max(total_series, 1)
            *
            100
        )


        stats_series["Catégorie"] = "Total"


        fig = px.bar(
            stats_series,
            x="Pourcentage",
            y="Catégorie",
            color="Statut",
            orientation="h",
            height=45,
            color_discrete_map={
                "Terminées": "#7987E8",
                "En cours": "#86D474",
                "À voir": "#FACD6B",
                "Stoppées": "#F55BA3"
            }
        )


        fig.update_layout(
            barmode="stack",
            showlegend=False,
            xaxis=dict(
                range=[0, 100],
                title=None,
                showticklabels=False
            ),
            yaxis=dict(
                title=None,
                showticklabels=False
            ),
            margin=dict(
                l=0,
                r=0,
                t=0,
                b=0
            )
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # =====================
        # KPI
        # =====================

        c1, c2, c3 = st.columns(3)


        with c1:
            st.markdown(
                f"""
                <div>
                    <div style="font-size:18px;color:#555;">
                        Total
                    </div>
                    <div style="font-size:28px;font-weight:600;">
                        {total_series}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with c2:
            st.markdown(
                f"""
                <div>
                    <div style="font-size:18px;color:#555;">
                        <span style="color:#7987E8;">●</span>
                        Terminées
                    </div>
                    <div style="font-size:28px;font-weight:600;">
                        {finished}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with c3:
            st.markdown(
                f"""
                <div>
                    <div style="font-size:18px;color:#555;">
                        <span style="color:#86D474;">●</span>
                        En cours
                    </div>
                    <div style="font-size:28px;font-weight:600;">
                        {watching}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)
        c4, c5, c6 = st.columns(3)


        with c4:
            st.markdown(
                f"""
                <div>
                    <div style="font-size:18px;color:#555;">
                        <span style="color:#FACD6B;">●</span>
                        À voir
                    </div>
                    <div style="font-size:28px;font-weight:600;">
                        {to_watch}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with c5:
            st.markdown(
                f"""
                <div>
                    <div style="font-size:18px;color:#555;">
                        <span style="color:#F55BA3;">●</span>
                        Stoppées
                    </div>
                    <div style="font-size:28px;font-weight:600;">
                        {stopped}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with c6:
            st.markdown(
                f"""
                <div>
                    <div style="font-size:18px;color:#555;">
                        <span style="color:#7987E8;">●</span>
                        Épisodes vus
                    </div>
                    <div style="font-size:28px;font-weight:600;">
                        {int(total_series_episodes_watched)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown(
        "<div style='height:20px'></div>",
        unsafe_allow_html=True
    )

# =====================
# Animés
# =====================

with col_animes:

    with st.container(border=True):

        st.subheader("Animés")

        total_animes = len(animes)

        watched = (
            animes["status"] == "watched"
        ).sum()

        watching = (
            animes["status"] == "continuing"
        ).sum()

        to_watch = (
            animes["status"] == "to_watch"
        ).sum()

        stopped = (
            animes["status"] == "stopped"
        ).sum()

        total_episodes_watched = (
            animes["progress"]
            .fillna(0)
            .sum()
        )


        stats_animes = pd.DataFrame(
            {
                "Statut": [
                    "Terminés",
                    "En cours",
                    "À voir",
                    "Stoppés"
                ],
                "Nombre": [
                    watched,
                    watching,
                    to_watch,
                    stopped
                ]
            }
        )


        stats_animes["Pourcentage"] = (
            stats_animes["Nombre"]
            /
            max(total_animes, 1)
            *
            100
        )


        stats_animes["Catégorie"] = "Total"


        fig = px.bar(
            stats_animes,
            x="Pourcentage",
            y="Catégorie",
            color="Statut",
            orientation="h",
            height=45,
            color_discrete_map={
                "Terminés": "#7987E8",
                "En cours": "#86D474",
                "À voir": "#FACD6B",
                "Stoppés": "#F55BA3"
            }
        )


        fig.update_layout(
            barmode="stack",
            showlegend=False,
            xaxis=dict(
                range=[0, 100],
                title=None,
                showticklabels=False
            ),
            yaxis=dict(
                title=None,
                showticklabels=False
            ),
            margin=dict(
                l=0,
                r=0,
                t=0,
                b=0
            )
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # =====================
        # KPI
        # =====================

        c1, c2, c3 = st.columns(3)


        with c1:
            st.markdown(
                f"""
                <div>
                    <div style="font-size:18px;color:#555;">
                        Total
                    </div>
                    <div style="font-size:28px;font-weight:600;">
                        {total_animes}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with c2:
            st.markdown(
                f"""
                <div>
                    <div style="font-size:18px;color:#555;">
                        <span style="color:#7987E8;">●</span>
                        Terminés
                    </div>
                    <div style="font-size:28px;font-weight:600;">
                        {watched}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with c3:
            st.markdown(
                f"""
                <div>
                    <div style="font-size:18px;color:#555;">
                        <span style="color:#86D474;">●</span>
                        En cours
                    </div>
                    <div style="font-size:28px;font-weight:600;">
                        {watching}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        st.markdown("<br>", unsafe_allow_html=True)


        c4, c5, c6 = st.columns(3)


        with c4:
            st.markdown(
                f"""
                <div>
                    <div style="font-size:18px;color:#555;">
                        <span style="color:#FACD6B;">●</span>
                        À voir
                    </div>
                    <div style="font-size:28px;font-weight:600;">
                        {to_watch}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with c5:
            st.markdown(
                f"""
                <div>
                    <div style="font-size:18px;color:#555;">
                        <span style="color:#F55BA3;">●</span>
                        Stoppés
                    </div>
                    <div style="font-size:28px;font-weight:600;">
                        {stopped}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with c6:
            st.markdown(
                f"""
                <div>
                    <div style="font-size:18px;color:#555;">
                        <span style="color:#7987E8;">●</span>
                        Épisodes vus
                    </div>
                    <div style="font-size:28px;font-weight:600;">
                        {int(total_episodes_watched)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        st.markdown(
            "<div style='height:20px'></div>",
            unsafe_allow_html=True
        )

# =====================
# DERNIÈRES SÉRIES VUES
# =====================

st.subheader("Dernières séries vues")


last_6_series = (
    series[
        series["last_watch"].notna()
    ]
    .sort_values(
        "last_watch",
        ascending=False
    )
    .head(6)
)


cols = st.columns(6)


for col, (_, serie) in zip(
    cols,
    last_6_series.iterrows()
):

    with col:

        # Titre
        st.markdown(
            f"""
            <div style="
                text-align:center;
                font-size:14px;
                font-weight:600;
                height:45px;
            ">
                {serie["title"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        # Affiche
        if pd.notna(serie.get("poster_path")) and serie["poster_path"] != "":

            poster_url = (
                "https://image.tmdb.org/t/p/w500"
                + serie["poster_path"]
            )

            st.image(
                poster_url,
                use_container_width=True
            )

        else:

            st.write("Pas d'affiche")

        # Dernier épisode vu
        last_episode = (
            serie["last_episode"]
            if pd.notna(serie["last_episode"])
            else "-"
        )

        st.markdown(
            f"""
            <div style="
                text-align:center;
                font-size:13px;
                color:gray;
            ">
                {last_episode}
            </div>
            """,
            unsafe_allow_html=True
        )

        # Date
        date_vue = serie["last_watch"].strftime("%d/%m/%Y")

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