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

livres["nombre de pages"] = pd.to_numeric(
    livres["nombre de pages"],
    errors="coerce"
)

livres["note"] = pd.to_numeric(
    livres["note"],
    errors="coerce"
)

livres_lus = livres[
    livres["statut"].astype(str).str.strip().str.lower() == "lu"
].copy()


annee_actuelle = 2026


livres_lus_cette_annee = livres_lus[
    livres_lus["date_fin"].dt.year == annee_actuelle
]


# =====================
# KPI
# =====================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Livres lus",
        len(livres_lus)
    )


with col2:

    pages_lues = livres_lus["nombre de pages"].sum()

    st.metric(
        "Pages lues",
        f"{pages_lues:,.0f}".replace(",", " ")
    )


with col3:

    st.metric(
        f"Livres lus en {annee_actuelle}",
        len(livres_lus_cette_annee)
    )


with col4:

    pages_lues_cette_annee = (
        livres_lus_cette_annee["nombre de pages"].sum()
    )

    st.metric(
        f"Pages lues en {annee_actuelle}",
        f"{pages_lues_cette_annee:,.0f}".replace(",", " ")
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

        # Titre
        st.markdown(
            f"**{livre['titre']}**"
        )

        # Auteur
        st.caption(
            str(livre["auteur"])
        )

        # Image
        image = livre["image de couverture"]

        if pd.notna(image) and str(image).strip():

            st.image(
                image,
                use_container_width=True
            )

        else:

            st.empty()

        # Date de fin
        st.caption(
            f"📅 {livre['date_fin'].strftime('%d/%m/%Y')}"
        )

        # Note
        if pd.notna(livre["note"]):

            st.caption(
                f"⭐ {livre['note']}/5"
            )

        else:

            st.caption("⭐ —")


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


st.line_chart(
    livres_par_mois,
    x_label="Mois",
    y_label="Livres terminés"
)


# =====================
# Tags les plus fréquents
# =====================

st.subheader("Tags les plus fréquents")


tags = (
    livres_lus["genres/tags"]
    .dropna()
    .astype(str)
)


tags_liste = []

for valeur in tags:

    for tag in valeur.split(","):

        tag = tag.strip()

        if tag:
            tags_liste.append(tag)


tags_frequents = (
    pd.Series(tags_liste)
    .value_counts()
    .head(10)
)


st.dataframe(
    tags_frequents.rename("Nombre de livres"),
    use_container_width=True
)