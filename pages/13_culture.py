
import gspread
import pandas as pd
import streamlit as st
import html
from google.oauth2.service_account import Credentials

# ==========================
# CONFIGURATION
# ==========================

st.set_page_config(
    page_title="Culture",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Wikicollection")


# --------------------------------------------------
# Configuration Google Sheets
# --------------------------------------------------

SHEET_ID_CULTURE = "11_RcYunE4kKJmF1Jo6g1MfoAy3di-S0j7BFDHWTdPh0"


@st.cache_resource
def get_sheet_culture():

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ]
    )

    client = gspread.authorize(credentials)

    return client.open_by_key(SHEET_ID_CULTURE).sheet1


@st.cache_data(ttl=300)
def load_culture_google_sheet():

    sheet = get_sheet_culture()

    data = sheet.get_all_records()

    return pd.DataFrame(data)


# --------------------------------------------------
# Affichage des données
# --------------------------------------------------

tableau = load_culture_google_sheet()

st.dataframe(
    tableau,
    use_container_width=True
)


# ==========================
# COLONNES ATTENDUES
# ==========================

COLONNES = [
    "Date",
    "Lien",
    "Titre",
    "Soustitre",
    "Resume",
    "Categorie1",
    "Categorie2",
    "Categorie3",
    "Liens",
    "Image",
]

colonnes_manquantes = [
    colonne
    for colonne in COLONNES
    if colonne not in tableau.columns
]

if colonnes_manquantes:

    st.error(
        "Colonnes manquantes : "
        + ", ".join(colonnes_manquantes)
    )

    st.stop()


# ==========================
# STYLE DES CARTES
# ==========================

st.markdown(
    """
    <style>

    /* Conteneur des cartes */

    div[class*="st-key-wiki_"] {

        background-color: #202129;
        border-radius: 14px;
        padding: 12px;

        height: 440px;
        min-height: 440px;
        max-height: 440px;

        overflow: hidden;
        box-sizing: border-box;
    }

    /* Réduction de l'espace entre les éléments */

    div[class*="st-key-wiki_"] [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
    }

    /* Titre */

    .wiki-titre {

        font-size: 17px;
        font-weight: 700;
        text-align: center;

        height: 48px;
        line-height: 24px;

        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 2;

        overflow: hidden;
        overflow-wrap: anywhere;

        margin-bottom: -10px !important;
    }

    /* Sous-titre */

    .wiki-soustitre {

        font-size: 13px;
        font-weight: 400;
        color: #b0b0b0;
        text-align: center;

        height: 38px;
        line-height: 19px;

        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 2;

        overflow: hidden;
        overflow-wrap: anywhere;

        margin-top: 0px !important;
        margin-bottom: 3px !important;
    }

    /* Image */

    div[class*="st-key-wiki_"] [data-testid="stImage"] {

        height: 155px;
        min-height: 155px;
        max-height: 155px;

        overflow: hidden;
        border-radius: 8px;

        margin: 0px !important;
    }

    div[class*="st-key-wiki_"] [data-testid="stImage"] img {

        width: 100%;
        height: 155px;

        object-fit: cover;
    }

    /* Résumé */

    .wiki-resume {

        font-size: 13px;
        line-height: 19px;

        height: 115px;
        max-height: 115px;

        overflow: hidden;

        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 6;
    }

    /* Date */

    .wiki-date {

        font-size: 12px;
        color: #999999;
        text-align: right;

        margin-top: 2px;
        margin-bottom: -5px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================
# NETTOYAGE DES DONNÉES
# ==========================

# Supprimer les lignes sans titre

tableau = tableau.dropna(
    subset=["Titre"]
).copy()

# Réinitialiser les index

tableau = tableau.reset_index(drop=True)


# ==========================
# AFFICHAGE EN 4 COLONNES
# ==========================

if tableau.empty:

    st.info("Aucune fiche dans ta collection.")

else:

    for debut in range(0, len(tableau), 4):

        elements_ligne = tableau.iloc[
            debut:debut + 4
        ]

        colonnes = st.columns(4, gap="medium")

        for index, (_, element) in enumerate(
            elements_ligne.iterrows()
        ):

            with colonnes[index]:

                # ----------------------------------
                # Récupération des informations
                # ----------------------------------

                titre = str(
                    element.get("Titre") or "Sans titre"
                )

                soustitre = str(
                    element.get("Soustitre") or ""
                )

                resume = str(
                    element.get("Resume") or ""
                )

                categorie1 = str(
                    element.get("Categorie1") or ""
                ).strip()

                categorie2 = str(
                    element.get("Categorie2") or ""
                ).strip()

                categorie3 = str(
                    element.get("Categorie3") or ""
                ).strip()

                lien = str(
                    element.get("Lien") or ""
                ).strip()

                liens = str(
                    element.get("Liens") or ""
                ).strip()

                image = str(
                    element.get("Image") or ""
                ).strip()

                date = element.get("Date")

                # ----------------------------------
                # Conversion de la date
                # ----------------------------------

                if pd.notna(date):

                    date_convertie = pd.to_datetime(
                        date,
                        dayfirst=True,
                        errors="coerce"
                    )

                    if pd.notna(date_convertie):

                        date = date_convertie.strftime(
                            "%d/%m/%Y"
                        )

                    else:

                        date = str(date)

                else:

                    date = ""

                # ----------------------------------
                # Carte
                # ----------------------------------

                with st.container(
                    key=f"wiki_{debut + index}",
                ):

                    # Titre

                    st.markdown(
                        f'<div class="wiki-titre">'
                        f'{html.escape(titre)}</div>',
                        unsafe_allow_html=True
                    )

                    # Sous-titre

                    st.markdown(
                        f'<div class="wiki-soustitre">'
                        f'{html.escape(soustitre)}</div>',
                        unsafe_allow_html=True
                    )

                    # Image

                    if image:

                        try:

                            st.image(
                                image,
                                use_container_width=True
                            )

                        except Exception:

                            st.markdown(
                                "🖼️ Image indisponible"
                            )

                    else:

                        st.markdown(
                            "🖼️ Image indisponible"
                        )

                    # Résumé

                    st.markdown(
                        f'<div class="wiki-resume">'
                        f'{html.escape(resume)}</div>',
                        unsafe_allow_html=True
                    )

                    # Date

                    st.markdown(
                        f'<div class="wiki-date">'
                        f'📅 {html.escape(date)}</div>',
                        unsafe_allow_html=True
                    )
