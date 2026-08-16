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
    errors="coerce",
    dayfirst=True
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


# =====================
# KPI
# =====================

livres_a_lire = livres[
    livres["statut"]
    .astype(str)
    .str.strip()
    .str.lower()
    .isin(["à lire", "pense-bête"])
]

livres_abandonnes = livres[
    livres["statut"].astype(str).str.strip().str.lower() == "abandonnés"
]


col1, col2, col3, col4, col5, col6 = st.columns(6)


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


with col5:

    st.metric(
        "Livres à lire",
        len(livres_a_lire)
    )


with col6:

    st.metric(
        "Livres abandonnés",
        len(livres_abandonnes)
    )

st.write("")
st.write("")
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

        # =====================
        # Titre
        # =====================

        st.markdown(
            f"""
            <div style="
                text-align: center;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                font-weight: 600;
                margin-bottom: 8px;
                height: 28px;
                line-height: 28px;
            ">
                {livre['titre']}
            </div>
            """,
            unsafe_allow_html=True
        )


        # =====================
        # Couverture
        # =====================

        image = livre["image de couverture"]

        if pd.notna(image) and str(image).strip():

            st.markdown(
                f"""
                <div style="
                    width: 100%;
                    height: 260px;
                    overflow: hidden;
                    border-radius: 8px;
                ">
                    <img
                        src="{image}"
                        style="
                            width: 100%;
                            height: 100%;
                            object-fit: cover;
                            object-position: center;
                            border-radius: 8px;
                        "
                    >
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div style="
                    width: 100%;
                    height: 240px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 8px;
                ">
                    Pas de couverture
                </div>
                """,
                unsafe_allow_html=True
            )


        # =====================
        # Date de fin
        # =====================

        st.markdown(
            f"""
            <div style="
                text-align: center;
                color: #666666;
                font-weight: 500;
                margin-top: 8px;
            ">
                {livre['date_fin'].strftime('%d/%m/%Y')}
            </div>
            """,
            unsafe_allow_html=True
        )

st.write("")
st.write("")
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
st.write("")
st.write("")

