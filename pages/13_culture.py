
import streamlit as st
import gspread
import pandas as pd
import html
import re
import json
import math


# ==================================================
# CONFIGURATION
# ==================================================

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


# ==================================================
# CONNEXION GOOGLE SHEETS
# ==================================================

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


# ==================================================
# CHARGEMENT DES DONNÉES
# ==================================================

df = load_culture_google_sheet()


# ==================================================
# COULEURS DES CATÉGORIES
# ==================================================

COULEURS_CATEGORIES = {
    "biologie": "#8EDE5B",
    "géographie": "#73ABF5",
    "geographie": "#73ABF5",
    "personne": "#F5D5AE",
}

COULEUR_DEFAUT = "#666875"


def obtenir_couleur(categorie):

    return COULEURS_CATEGORIES.get(
        str(categorie).strip().lower(),
        COULEUR_DEFAUT
    )


# ==================================================
# FONCTIONS UTILITAIRES
# ==================================================

def valeur_texte(valeur):

    if pd.isna(valeur):
        return ""

    return str(valeur).strip()


def extraire_liens(valeur):
    """
    Récupère les titres présents dans la colonne Liens.

    Séparateurs acceptés :
    - virgule
    - point-virgule
    - retour à la ligne
    - barre verticale

    Accepte également une liste au format JSON.
    """

    texte = valeur_texte(valeur)

    if not texte:
        return []

    # Essai de lecture d'une liste JSON
    if texte.startswith("[") and texte.endswith("]"):

        try:

            resultat = json.loads(texte)

            if isinstance(resultat, list):

                return [
                    str(element).strip()
                    for element in resultat
                    if str(element).strip()
                ]

        except (json.JSONDecodeError, TypeError):
            pass

    # Séparation des titres
    elements = re.split(r"[;,\n|]+", texte)

    return [
        element.strip().strip('"').strip("'")
        for element in elements
        if element.strip()
    ]


# ==================================================
# CONSTRUCTION DES CONNEXIONS
# ==================================================

def construire_connexions(dataframe):

    titres = {}

    for index, ligne in dataframe.iterrows():

        titre = valeur_texte(ligne["Titre"])

        if titre:

            cle = titre.casefold()

            if cle not in titres:
                titres[cle] = index

    connexions = {
        index: set()
        for index in dataframe.index
    }

    # Lecture des liens déclarés par chaque fiche
    for index, ligne in dataframe.iterrows():

        liens = extraire_liens(ligne["Liens"])

        for titre_lie in liens:

            cle = titre_lie.casefold()

            if cle not in titres:
                continue

            index_lie = titres[cle]

            if index_lie == index:
                continue

            # Connexion dans les deux sens
            connexions[index].add(index_lie)
            connexions[index_lie].add(index)

    return connexions


connexions = construire_connexions(df)


# ==================================================
# CSS
# ==================================================

st.markdown("""
<style>

/* ==================================================
   CARTES DU MODE FICHES
   ================================================== */

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

/* Ligne du bas */
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


/* ==================================================
   MODE CONNEXIONS
   ================================================== */

.connexion-sous-titre {
    font-size: 13px;
    color: #999999;
    text-align: center;
    margin-bottom: 15px;
}

.connexion-info {
    background-color: #202129;
    border-radius: 10px;
    padding: 12px;
    text-align: center;
    color: #aaaaaa;
    font-size: 13px;
}

/* Liste des fiches */
div[class*="st-key-selection_fiche_"] button {
    text-align: left !important;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# EN-TÊTE ET CHOIX DE L'AFFICHAGE
# ==================================================

col_titre, col_mode = st.columns([3, 2])

with col_titre:

    st.title("Wikicollection")

with col_mode:

    mode = st.radio(
        "Affichage",
        ["Fiches", "Connexions"],
        horizontal=True,
        label_visibility="collapsed",
        key="mode_wikicollection"
    )


# ==================================================
# MODE 1 : FICHES
# ==================================================

if mode == "Fiches":

    for debut in range(0, len(df), 4):

        colonnes = st.columns(4, gap="medium")

        for index, colonne in enumerate(colonnes):

            position = debut + index

            if position >= len(df):
                break

            ligne = df.iloc[position]

            # Récupération des données
            date = valeur_texte(ligne["Date"])
            lien = valeur_texte(ligne["Lien"])
            titre = valeur_texte(ligne["Titre"])
            soustitre = valeur_texte(ligne["Soustitre"])
            resume = valeur_texte(ligne["Resume"])
            categorie1 = valeur_texte(ligne["Categorie1"])
            image = valeur_texte(ligne["Image"])

            # Couleur du bandeau
            couleur_bandeau = obtenir_couleur(categorie1)

            # Sécurisation HTML
            titre_securise = html.escape(titre)
            soustitre_securise = html.escape(soustitre)
            resume_securise = html.escape(resume)
            date_securisee = html.escape(date)

            lien_securise = html.escape(
                lien.strip(),
                quote=True
            )

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
                    if image.startswith(("https://", "http://")):

                        st.markdown(
                            f'<img class="wiki-image" '
                            f'src="{html.escape(image, quote=True)}">',
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
                    if lien.startswith(("https://", "http://")):

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


# ==================================================
# MODE 2 : CONNEXIONS
# ==================================================

elif mode == "Connexions":

    # Initialisation de la fiche sélectionnée
    if "fiche_selectionnee" not in st.session_state:

        st.session_state.fiche_selectionnee = (
            df.index[0] if len(df) > 0 else None
        )

    # Vérification de la sélection
    if (
        st.session_state.fiche_selectionnee not in df.index
        and len(df) > 0
    ):

        st.session_state.fiche_selectionnee = df.index[0]

    # Deux zones :
    # Graphique à gauche, liste des titres à droite
    col_graphique, col_liste = st.columns([4, 1.5])


    # --------------------------------------------------
    # GRAPHIQUE DES CONNEXIONS
    # --------------------------------------------------

    with col_graphique:

        if len(df) == 0:

            st.info("Aucune fiche disponible.")

        else:

            index_selectionne = st.session_state.fiche_selectionnee

            fiche = df.loc[index_selectionne]

            titre_selectionne = valeur_texte(fiche["Titre"])

            categorie_selectionnee = valeur_texte(
                fiche["Categorie1"]
            )

            couleur_centrale = obtenir_couleur(
                categorie_selectionnee
            )

            st.markdown(
                '<div class="connexion-sous-titre">'
                'Explore les relations entre les fiches'
                '</div>',
                unsafe_allow_html=True
            )

            # Fiches connectées
            indices_lies = sorted(
                connexions.get(index_selectionne, set()),
                key=lambda i: valeur_texte(
                    df.loc[i, "Titre"]
                ).casefold()
            )


            # --------------------------------------------------
            # CRÉATION DES NŒUDS
            # --------------------------------------------------

            def creer_noeud(titre, couleur, taille=10):

                titre_html = html.escape(
                    titre,
                    quote=False
                )

                return (
                    '<<TABLE BORDER="0" CELLBORDER="0" '
                    'CELLSPACING="0" CELLPADDING="0" '
                    'BGCOLOR="#202129">'
                    '<TR>'
                    f'<TD WIDTH="5" BGCOLOR="{couleur}"></TD>'
                    '<TD CELLPADDING="10" BGCOLOR="#202129">'
                    f'<FONT COLOR="#FFFFFF" POINT-SIZE="{taille}">'
                    f'{titre_html}'
                    '</FONT>'
                    '</TD>'
                    '</TR>'
                    '</TABLE>>'
                )


            # --------------------------------------------------
            # CONSTRUCTION DU GRAPHIQUE
            # --------------------------------------------------

            lignes_graphique = [
                "graph Connexions {",
                'layout=neato;',
                'overlap=false;',
                'splines=true;',
                'bgcolor="transparent";',
                'outputorder=edgesfirst;',
                'pad=0.5;',
                'sep="+20";',
                'node [shape=plain, fontname="Arial"];',
                'edge [color="#555963", penwidth=1.2];'
            ]


            # --------------------------------------------------
            # FICHE CENTRALE
            # --------------------------------------------------

            lignes_graphique.append(
                'centre ['
                f'label={creer_noeud(titre_selectionne, couleur_centrale, 11)}, '
                'pos="0,0!", '
                'pin=true'
                '];'
            )


            # --------------------------------------------------
            # FICHES AUTOUR DU CENTRE
            # --------------------------------------------------

            nombre = len(indices_lies)

            rayon = 3.2

            for numero, index_lie in enumerate(indices_lies):

                fiche_liee = df.loc[index_lie]

                titre_lie = valeur_texte(
                    fiche_liee["Titre"]
                )

                categorie_liee = valeur_texte(
                    fiche_liee["Categorie1"]
                )

                couleur_liee = obtenir_couleur(
                    categorie_liee
                )

                # Positionnement circulaire
                angle = (
                    2 * math.pi * numero / max(nombre, 1)
                ) - math.pi / 2

                x = rayon * math.cos(angle)
                y = rayon * math.sin(angle)

                identifiant = f"fiche_{numero}"

                lignes_graphique.append(
                    f'{identifiant} ['
                    f'label={creer_noeud(titre_lie, couleur_liee, 10)}, '
                    f'pos="{x:.3f},{y:.3f}!", '
                    'pin=true'
                    '];'
                )

                # Liaison avec la fiche centrale
                lignes_graphique.append(
                    f'centre -- {identifiant};'
                )

            lignes_graphique.append("}")

            graphique = "\n".join(lignes_graphique)


            # --------------------------------------------------
            # AFFICHAGE DU GRAPHIQUE
            # --------------------------------------------------

            if indices_lies:

                st.graphviz_chart(
                    graphique,
                    use_container_width=True
                )

                st.markdown(
                    f'<div class="connexion-info">'
                    f'{len(indices_lies)} fiche(s) connectée(s) à '
                    f'<strong>{html.escape(titre_selectionne)}</strong>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f'<div class="connexion-info">'
                    f'<strong>{html.escape(titre_selectionne)}</strong>'
                    f'<br><br>'
                    f'Aucune connexion trouvée pour cette fiche.'
                    f'</div>',
                    unsafe_allow_html=True
                )


    # --------------------------------------------------
    # LISTE DES TITRES À DROITE
    # --------------------------------------------------

    with col_liste:

        st.markdown("### Toutes les fiches")

        with st.container(height=650):

            for index, ligne in df.iterrows():

                titre = valeur_texte(ligne["Titre"])

                if not titre:
                    continue

                est_selectionne = (
                    index == st.session_state.fiche_selectionnee
                )

                if st.button(
                    titre,
                    key=f"selection_fiche_{index}",
                    type="primary" if est_selectionne else "secondary",
                    use_container_width=True
                ):

                    st.session_state.fiche_selectionnee = index

                    st.rerun()
