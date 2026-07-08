import streamlit as st
import pandas as pd

from scripts.importation_tvtime import tab_tv
from scripts.importation_myanimelist import tab_myanimelist

movies, series, series_episodes = tab_tv()
animes = tab_myanimelist()


st.title("🍿 Watchlist")


# =====================
# Dashboard
# =====================

# Nombre de films vus
nb_movies_watched = (
    movies["status"] == "watched"
).sum()

# Nombre de séries terminées
nb_series_finished = (
    series["status"] == "up_to_date"
).sum()

# Nombre de séries jamais terminées
nb_series_unfinished = (
    series["status"].isin(["continuing", "stopped"])
).sum()


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Films vus",
        nb_movies_watched
    )

with col2:
    st.metric(
        "Séries terminées",
        nb_series_finished
    )

with col3:
    st.metric(
        "Séries non terminées",
        nb_series_unfinished
    )

# =====================
# Cartes Anime / Séries
# =====================

st.header("📊 Statistiques")

col_series, col_animes = st.columns(2)


# =====================
# Séries
# =====================

with col_series:
    with st.container(border=True):
        st.subheader("📺 Séries")

        total_series = len(series)

        finished = (
            series["status"] == "up_to_date"
        ).sum()

        watching = (
            series["status"] == "continuing"
        ).sum()

        stopped = (
            series["status"] == "stopped"
        ).sum()


        stats_series = pd.DataFrame({
            "Statut": [
                "Terminés",
                "En cours",
                "Stoppés"
            ],
            "Nombre": [
                finished,
                watching,
                stopped
            ]
        })


        stats_series["Pourcentage"] = (
            stats_series["Nombre"] / total_series * 100
        )


        # Graphique en haut
        import plotly.express as px

        stats_series["Catégorie"] = "Total"

        fig = px.bar(
            stats_series,
            x="Pourcentage",
            y="Catégorie",
            color="Statut",
            orientation="h",
            height=45,
            color_discrete_map={
                "Terminés": "#7987E8",
                "En cours": "#86D474",
                "Stoppés": "#F55BA3"
            }
        )

        fig.update_layout(
            barmode="stack",
            showlegend=False,
            xaxis={
                "range": [0, 100],
                "title": None,
                "showticklabels": False
            },
            yaxis={
                "title": None,
                "showticklabels": False
            },
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


        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Total",
                total_series
            )

        with c2:
            st.markdown(
                f"""
                <div style="font-size:14px;">
                    <span style="color:#7987E8; font-size:22px;">●</span>
                    Terminés
                </div>
                <div style="font-size:28px; font-weight:600;">
                    {finished}
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                f"""
                <div style="font-size:14px;">
                    <span style="color:#86D474; font-size:22px;">●</span>
                    En cours
                </div>
                <div style="font-size:28px; font-weight:600;">
                    {watching}
                </div>
                """,
                unsafe_allow_html=True
            )


        c4, c5 = st.columns(2)

        with c4:
            st.markdown(
                f"""
                <div style="font-size:14px;">
                    <span style="color:#F55BA3; font-size:22px;">●</span>
                    Stoppés
                </div>
                <div style="font-size:28px; font-weight:600;">
                    {stopped}
                </div>
                """,
                unsafe_allow_html=True
            )



# =====================
# Animés
# =====================

with col_animes:
    with st.container(border=True):
        st.subheader("🍥 Animés")

        total_animes = len(animes)

        watched = (
            animes["status"] == "watched"
        ).sum()

        watching = (
            animes["status"] == "continuing"
        ).sum()

        stopped = (
            animes["status"] == "stopped"
        ).sum()

        paused = (
            animes["status"] == "paused"
        ).sum()

        total_episodes_watched = animes["progress"].sum()


        stats_animes = pd.DataFrame({
            "Statut": [
                "Terminés",
                "En cours",
                "En pause",
                "Stoppés"
            ],
            "Nombre": [
                watched,
                watching,
                paused,
                stopped
            ]
        })


        stats_animes["Pourcentage"] = (
            stats_animes["Nombre"] / total_animes * 100
        )


        # Graphique en haut
        import plotly.express as px

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
                "En pause": "#FACD6B",
                "Stoppés": "#F55BA3"
            }
        )

        fig.update_layout(
            barmode="stack",
            showlegend=False,
            xaxis={
                "range": [0, 100],
                "title": None,
                "showticklabels": False
            },
            yaxis={
                "title": None,
                "showticklabels": False
            },
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


        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Total",
                total_animes
            )

        with c2:
            st.markdown(
                f"""
                <div style="font-size:14px;">
                    <span style="color:#7987E8; font-size:22px;">●</span>
                    Terminés
                </div>
                <div style="font-size:28px; font-weight:600;">
                    {watched}
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                f"""
                <div style="font-size:14px;">
                    <span style="color:#86D474; font-size:22px;">●</span>
                    En cours
                </div>
                <div style="font-size:28px; font-weight:600;">
                    {watching}
                </div>
                """,
                unsafe_allow_html=True
            )


        c4, c5, c6 = st.columns(3)

        with c4:
            st.markdown(
                f"""
                <div style="font-size:14px;">
                    <span style="color:#FACD6B; font-size:22px;">●</span>
                    En pause
                </div>
                <div style="font-size:28px; font-weight:600;">
                    {paused}
                </div>
                """,
                unsafe_allow_html=True
            )

        with c5:
            st.markdown(
                f"""
                <div style="font-size:14px;">
                    <span style="color:#F55BA3; font-size:22px;">●</span>
                    Stoppés
                </div>
                <div style="font-size:28px; font-weight:600;">
                    {stopped}
                </div>
                """,
                unsafe_allow_html=True
            )

        with c6:
            st.metric(
                "Épisodes vus",
                int(total_episodes_watched)
            )

# =====================
# Films vus par mois
# =====================

movies_by_month = (
    movies[
        (movies["status"] == "watched")
        & (movies["watched_at"] >= "2023-01-01")
    ]
    .assign(month=lambda x: x["watched_at"].dt.to_period("M").astype(str))
    .groupby("month")
    .size()
)

st.subheader("Films vus par mois")

st.line_chart(movies_by_month)

# Nombre de films vus
nb_movies_watched = len(
    movies[movies["status"] == "watched"]
)

from scripts.gestion_watchlist import derniers_visionnages

watchlist = derniers_visionnages(movies, series)

st.header("Derniers visionnages")

st.dataframe(
    watchlist,
    use_container_width=True,
    hide_index=True
)


# =====================
# Tableaux de données
# =====================
st.header("Animes")

st.dataframe(
    animes,
    use_container_width=True,
    hide_index=True
)

st.header("Séries")
st.dataframe(
    series,
    use_container_width=True
)

st.header("Épisodes de séries")
st.dataframe(
    series_episodes,
    use_container_width=True
)

st.header("Animés")

from scripts.importation_anilist import load_anilist

anime = load_anilist("Poupette")

st.dataframe(anime)





st.header("Films")
st.dataframe(
    movies,
    use_container_width=True
)
