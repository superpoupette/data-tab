import streamlit as st
import pandas as pd

from scripts.data_loader import load_babelio


st.set_page_config(
    page_title="Bibliothèque",
    page_icon="📚",
    layout="wide"
)


st.title("📚 Bibliothèque")


# =====================
# Chargement des données
# =====================

livres = load_babelio().copy()


# =====================
# Préparation des données
# =====================

livres["date_fin"] = pd.to_datetime(
    livres["date de fin de lecture"],
    errors="coerce"
)

livres_lus = livres[
    livres["statut"].astype(str).str.strip().str.lower() == "lu"
].copy()


# =====================
# KPI
# =====================

annee_actuelle = 2026

livres_lus_cette_annee = livres_lus[
    livres_lus["date_fin"].dt.year == annee_actuelle
]


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Livres lus",
        len(livres_lus)
    )


with col2:

    st.metric(
        f"Livres lus en {annee_actuelle}",
        len(livres_lus_cette_annee)
    )


# =====================
# Derniers livres terminés
# =====================

st.subheader("Derniers livres terminés")


derniers_livres = (
    livres_lus[
        livres_lus["date_fin"].notna()
    ]
    .sort_values(
        "date_fin",
        ascending=False
    )
    .head(6)
)


colonnes = st.columns(6)


for col, (_, livre) in zip(
    colonnes,
    derniers_livres.iterrows()
):

    with col:

        image = livre["image de couverture"]

        if pd.notna(image) and str(image).strip():
            st.image(
                image,
                use_container_width=True
            )

        st.markdown(
            f"**{livre['titre']}**"
        )

        st.caption(
            str(livre["auteur"])
        )

        st.caption(
            livre["date_fin"].strftime("%d/%m/%Y")
        )


# =====================
# Livres terminés par mois
# =====================

st.subheader("Livres terminés par mois")


livres_avec_date = livres_lus[
    livres_lus["date_fin"].notna()
].copy()


livres_avec_date["mois"] = (
    livres_avec_date["date_fin"]
    .dt.to_period("M")
    .astype(str)
)


livres_par_mois = (
    livres_avec_date
    .groupby("mois")
    .size()
)


st.bar_chart(
    livres_par_mois,
    x_label="Mois",
    y_label="Livres terminés"
)