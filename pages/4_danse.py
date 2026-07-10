import streamlit as st
import pandas as pd
import plotly.express as px

from scripts.danse.google_sheet import load_danse_google_sheet


# =========================
# Chargement Google Sheet
# =========================

danse_recap = load_danse_google_sheet()


danse_recap["date_debut"] = pd.to_datetime(
    danse_recap["date_debut"],
    errors="coerce"
)

danse_recap["date_fin"] = pd.to_datetime(
    danse_recap["date_fin"],
    errors="coerce"
)


# Valeurs numériques

for col in [
    "duree_apprentissage",
    "nombre_seance",
    "duree_seance"
]:
    danse_recap[col] = pd.to_numeric(
        danse_recap[col],
        errors="coerce"
    ).fillna(0)



st.title("💃 Dashboard Danse")



# =========================
# Indicateurs principaux
# =========================

col1, col2, col3, col4 = st.columns(4)


with col1:

    temps_total_min = (
        danse_recap["duree_apprentissage"]
        .sum()
    )

    heures = int(
        temps_total_min // 60
    )

    minutes = int(
        temps_total_min % 60
    )

    st.metric(
        "Temps d'apprentissage global",
        f"{heures}h{minutes:02d}"
    )



with col2:

    nb_chorees = (
        danse_recap["duree_apprentissage"] > 0
    ).sum()

    st.metric(
        "Chorégraphies apprises",
        nb_chorees
    )



with col3:

    nb_sessions = (
        danse_recap["nombre_seance"]
        .sum()
    )

    st.metric(
        "Nombre de séances",
        int(nb_sessions)
    )



with col4:

    duree_moyenne = (
        danse_recap["duree_seance"]
        .mean()
    )

    st.metric(
        "Durée moyenne séance",
        f"{duree_moyenne:.0f} min"
    )



# =========================
# Graphiques principaux
# =========================


col1, col2 = st.columns(2)



# -------------------------
# Styles
# -------------------------

with col1:

    st.subheader(
        "Répartition des styles"
    )


    styles = (
        danse_recap
        .groupby("style")
        .size()
        .reset_index(
            name="nombre"
        )
        .sort_values(
            "nombre",
            ascending=False
        )
    )


    fig_style = px.pie(
        styles,
        values="nombre",
        names="style",
        hole=0.3
    )


    st.plotly_chart(
        fig_style,
        use_container_width=True
    )



# -------------------------
# Artistes
# -------------------------

with col2:

    st.subheader(
        "Top 10 artistes"
    )


    artistes = (
        danse_recap[
            danse_recap["duree_apprentissage"] > 0
        ]
        .groupby("artiste")
        .size()
        .reset_index(
            name="nombre_chorees"
        )
        .sort_values(
            "nombre_chorees",
            ascending=False
        )
        .head(10)
    )


    fig_artistes = px.bar(
        artistes,
        x="nombre_chorees",
        y="artiste",
        orientation="h",
        labels={
            "nombre_chorees":
                "Nombre de chorégraphies",
            "artiste":
                "Artiste"
        }
    )


    st.plotly_chart(
        fig_artistes,
        use_container_width=True
    )



# =========================
# Evolution des apprentissages
# =========================

st.subheader(
    "Chorégraphies commencées par mois"
)


evolution = (
    danse_recap
    .dropna(
        subset=[
            "date_debut"
        ]
    )
    .assign(
        mois=lambda x:
            x["date_debut"]
            .dt.to_period("M")
            .astype(str)
    )
    .groupby("mois")
    .size()
    .reset_index(
        name="nombre"
    )
)


fig_mois = px.line(
    evolution,
    x="mois",
    y="nombre",
    markers=True,
    labels={
        "mois":
            "Mois",
        "nombre":
            "Nouvelles chorégraphies"
    }
)


st.plotly_chart(
    fig_mois,
    use_container_width=True
)



# =========================
# Top chorégraphies
# =========================

st.subheader(
    "Top 10 chorégraphies par temps d'apprentissage"
)


top_chorees = (
    danse_recap
    .sort_values(
        "duree_apprentissage",
        ascending=False
    )
    .head(10)
)


fig_top = px.bar(
    top_chorees,
    y="titre",
    x="duree_apprentissage",
    orientation="h",
    labels={
        "titre":
            "Chorégraphie",
        "duree_apprentissage":
            "Temps (min)"
    }
)


st.plotly_chart(
    fig_top,
    use_container_width=True
)



# =========================
# Tableau
# =========================

st.subheader(
    "Récapitulatif des chorégraphies"
)


st.dataframe(
    danse_recap,
    use_container_width=True,
    hide_index=True
)