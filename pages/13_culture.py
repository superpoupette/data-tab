
import streamlit as st
import gspread
import pandas as pd
import html

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

SHEET_ID = "11_RcYunE4kKJmF1Jo6g1MfoAy3di-S0j7BFDHWTdPh0"

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


# --------------------------------------------------
# CONNEXION GOOGLE SHEETS
# --------------------------------------------------

@st.cache_resource
def get_sheet_culture():
    credentials = st.secrets["gcp_service_account"]

    client = gspread.service_account_from_dict(credentials)

    spreadsheet = client.open_by_key(SHEET_ID)

    return spreadsheet.sheet1


@st.cache_data(ttl=300)
def load_culture_google_sheet():
    sheet = get_sheet_culture()

    data = sheet.get_all_records()

    df = pd.DataFrame(data)

    # Garantit la présence de toutes les colonnes
    for colonne in COLONNES:
        if colonne not in df.columns:
            df[colonne] = ""

    return df[COLONNES]


# --------------------------------------------------
# CHARGEMENT DES DONNÉES
# --------------------------------------------------

df = load_culture_google_sheet()


# --------------------------------------------------
# COULEURS DES CATÉGORIES
# --------------------------------------------------

COULEURS_CATEGORIES = {
    "biologie": "#3BA66B",
    "géographie": "#3185D8",
    "geographie": "#3185D8",
    "personne": "#9564C8",
}

COULEUR_DEFAUT = "#666875"


# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>

/* Carte */
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

/* Espacement interne */
div[class*="st-key-wiki_"] [data-testid="stVerticalBlock"] {
    gap: 0rem !important;
}

/* Bandeau supérieur */
.wiki-bandeau {
    height: 6px;
    width: calc(100% + 24px);
    margin: -12px -12px 10px -12px;
    border-radius: 14px 14px 0 0;
}

/* Titre */
.wiki-titre {
    font-size: 17px;
    font-weight: 700;
    text-align: center;
    line-height: 24px;
    height: 48px;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    margin-bottom: -10px !important;
}

/* Sous-titre */
.wiki-soustitre {
    font-size: 13px;
    font-weight: 400;
    color: #b0b0b0;
    text-align: center;
    line-height: 19px;
    height: 38px;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    margin-top: 0 !important;
    margin-bottom: 3px !important;
}

/* Image */
.wiki-image {
    width: 100%;
    height: 155px;
    object-fit: cover;
    border-radius: 8px;
    display: block;
}

/* Résumé */
.wiki-resume {
    font-size: 13px;
    line-height: 19px;
    height: 115px;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 6;
    -webkit-box-orient: vertical;
}

/* Ligne du bas : bouton et date */
.wiki-bas {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin-top: 2px;
}

/* Bouton Wiki */
.wiki-bouton {
    display: inline-block;
    background-color: #343642;
    color: #ffffff !important;
    text-decoration: none !important;
    font-size: 12px;
    font-weight: 600;
    padding: 6px 10px;
    border-radius: 7px;
    transition: background-color 0.2s;
}

.wiki-bouton:hover {
    background-color: #484c5c;
    color: #ffffff !important;
}

/* Date */
.wiki-date {
    font-size: 12px;
    color: #999999;
    text-align: right;
    white-space: nowrap;
    margin: 0;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# AFFICHAGE DES CARTES
# --------------------------------------------------

st.title("Culture / Wikicollection")

# 4 colonnes
colonnes = st.columns(4, gap="medium")

for debut in range(0, len(df), 4):

    # Nouvelle ligne de 4 cartes
    colonnes = st.columns(4, gap="medium")

    for index, colonne in enumerate(colonnes):

        position = debut + index

        if position >= len(df):
            break

        ligne = df.iloc[position]

        # Récupération des données
        date = str(ligne["Date"]) if pd.notna(ligne["Date"]) else ""
        lien = str(ligne["Lien"]) if pd.notna(ligne["Lien"]) else ""
        titre = str(ligne["Titre"]) if pd.notna(ligne["Titre"]) else ""
        soustitre = str(ligne["Soustitre"]) if pd.notna(ligne["Soustitre"]) else ""
        resume = str(ligne["Resume"]) if pd.notna(ligne["Resume"]) else ""
        categorie1 = str(ligne["Categorie1"]) if pd.notna(ligne["Categorie1"]) else ""
        image = str(ligne["Image"]) if pd.notna(ligne["Image"]) else ""

        # Couleur du bandeau selon Categorie1
        couleur_bandeau = COULEURS_CATEGORIES.get(
            categorie1.strip().lower(),
            COULEUR_DEFAUT
        )

        # Sécurisation des textes HTML
        titre_securise = html.escape(titre)
        soustitre_securise = html.escape(soustitre)
        resume_securise = html.escape(resume)
        date_securisee = html.escape(date)

        # Vérification du lien
        lien_securise = html.escape(lien.strip(), quote=True)

        with colonne:

            with st.container(key=f"wiki_{position}"):

                # Bandeau coloré
                st.markdown(
                    f'<div class="wiki-bandeau" '
                    f'style="background-color: {couleur_bandeau};">'
                    f'</div>',
                    unsafe_allow_html=True
                )

                # Titre
                st.markdown(
                    f'<div class="wiki-titre">'
                    f'{titre_securise}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                # Sous-titre
                st.markdown(
                    f'<div class="wiki-soustitre">'
                    f'{soustitre_securise}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                # Image
                if image.strip().startswith(("https://", "http://")):
                    st.markdown(
                        f'<img class="wiki-image" '
                        f'src="{html.escape(image.strip(), quote=True)}">',
                        unsafe_allow_html=True
                    )

                # Résumé
                st.markdown(
                    f'<div class="wiki-resume">'
                    f'{resume_securise}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                # Bouton Wiki
                if lien.strip().startswith(("https://", "http://")):

                    bouton_wiki = (
                        f'<a class="wiki-bouton" '
                        f'href="{lien_securise}" '
                        f'target="_blank" '
                        f'rel="noopener noreferrer">'
                        f'↗ Wiki'
                        f'</a>'
                    )

                else:
                    bouton_wiki = ""

                # Bouton à gauche et date à droite
                st.markdown(
                    f'<div class="wiki-bas">'
                    f'{bouton_wiki}'
                    f'<div class="wiki-date">'
                    f'{date_securisee}'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
