import gspread
import pandas as pd
import streamlit as st
from datetime import date, datetime
import html

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DOSSIER_IMAGES = BASE_DIR / "images" / "succes"

from google.oauth2.service_account import Credentials


# --------------------------------------------------
# Configuration Google Sheets
# --------------------------------------------------

SHEET_ID = "1rec6RNx7eViF3XxYovrVdGmsu22PXP0GoLDNVc0JNJg"


def get_sheet():

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ]
    )

    client = gspread.authorize(credentials)

    return client.open_by_key(SHEET_ID).sheet1


def load_succes_google_sheet():

    sheet = get_sheet()

    data = sheet.get_all_records()

    return pd.DataFrame(data)


# --------------------------------------------------
# Chargement des succès
# --------------------------------------------------

COLONNES_ATTENDUES = [
    "nom",
    "categorie",
    "date_creation",
    "date_debut_validation",
    "date_fin_validation",
    "image",
    "compteur",
    "succes",
    "etoiles",
    "details",
]

try:
    tableau = load_succes_google_sheet()

except Exception as erreur:
    st.error(
        f"Impossible de charger les succès depuis Google Sheets : {erreur}"
    )
    st.stop()


# Vérification des colonnes
colonnes_manquantes = [
    colonne
    for colonne in COLONNES_ATTENDUES
    if colonne not in tableau.columns
]

if colonnes_manquantes:
    st.error(
        "Colonnes manquantes dans Google Sheets : "
        + ", ".join(colonnes_manquantes)
    )
    st.stop()


# Conserve les colonnes attendues et leur ordre
elements = (
    tableau[COLONNES_ATTENDUES]
    .to_dict(orient="records")
)


# --------------------------------------------------
# Images par défaut selon la catégorie
# --------------------------------------------------

IMAGES_DEFAUT = {
    "sport": "sport.png",
    "dessin": "dessin.png",
    "danse": "danse.png",
    "creatif": "creatif.png",
    "divers": "divers.png",
    "bienetre": "bienetre.png",
    "culture": "culture.png",
}


# --------------------------------------------------
# Conversion des dates
# --------------------------------------------------

def convertir_date(valeur):
    """Convertit les dates Excel ou les chaînes en datetime."""

    if valeur is None:
        return None

    try:
        if pd.isna(valeur):
            return None
    except (TypeError, ValueError):
        return None

    # Excel peut fournir directement un objet datetime
    if isinstance(valeur, datetime):
        return valeur.replace(tzinfo=None)

    if isinstance(valeur, date):
        return datetime.combine(valeur, datetime.min.time())

    valeur = str(valeur).strip()

    if not valeur:
        return None

    # Formats courants
    formats_dates = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M",
        "%d-%m-%Y %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
    ]

    for format_date in formats_dates:
        try:
            return datetime.strptime(valeur, format_date)
        except ValueError:
            continue

    # Dernière tentative : format ISO avec heure ou fuseau
    try:
        resultat = datetime.fromisoformat(
            valeur.replace("Z", "+00:00")
        )

        if resultat.tzinfo is not None:
            resultat = resultat.replace(tzinfo=None)

        return resultat

    except (ValueError, TypeError):
        return None


def afficher_date(valeur):
    """Affiche une date au format JJ/MM/AAAA."""

    date_convertie = convertir_date(valeur)

    if date_convertie is not None:
        return date_convertie.strftime("%d/%m/%Y")

    if valeur is None:
        return ""

    try:
        if pd.isna(valeur):
            return ""
    except (TypeError, ValueError):
        pass

    return str(valeur).strip()


# --------------------------------------------------
# Normalisation des données Excel
# --------------------------------------------------

for element in elements:

    # Normalisation de la valeur de succès
    valeur_succes = element.get("succes")

    if isinstance(valeur_succes, str):
        element["succes"] = (
            valeur_succes.strip().lower()
            in ("true", "vrai", "1", "oui", "yes")
        )
    elif valeur_succes is None or pd.isna(valeur_succes):
        element["succes"] = False
    else:
        element["succes"] = valeur_succes is True or (
            isinstance(valeur_succes, (int, float))
            and valeur_succes == 1
        )



# --------------------------------------------------
# Compteur d'étoiles, tri et filtre par année
# --------------------------------------------------

def convertir_etoiles(valeur):
    """Convertit le nombre d'étoiles en entier sans erreur."""
    if valeur is None:
        return 0

    try:
        if pd.isna(valeur):
            return 0
        return int(float(valeur))
    except (ValueError, TypeError, OverflowError):
        return 0


# Conserver la liste complète pour calculer les années disponibles
elements_complets = elements.copy()

# Total des étoiles acquises, indépendamment du filtre
total_etoiles = sum(
    convertir_etoiles(element.get("etoiles"))
    for element in elements_complets
    if element.get("succes") is True
)

# Années disponibles à partir des dates de création
annees = sorted({
    date_creation.year
    for element in elements_complets
    if (
        date_creation := convertir_date(element.get("date_creation"))
    ) is not None
}, reverse=True)

# Trois commandes sur la même ligne
col_etoiles, col_tri, col_annee = st.columns(
    [1, 2, 1],
    vertical_alignment="center",
)

with col_etoiles:
    st.markdown(f"### ⭐ {total_etoiles}")

with col_tri:
    ordre_tri = st.selectbox(
        "Trier par :",
        options=[
            "Date de création",
            "Date de validation",
            "Catégorie",
        ],
        label_visibility="collapsed",
    )

with col_annee:
    annee_selectionnee = st.selectbox(
        "Année :",
        options=["Toutes les années"] + annees,
        label_visibility="collapsed",
    )


# --------------------------------------------------
# Filtre par année de création
# --------------------------------------------------

elements_filtres = elements_complets.copy()

if annee_selectionnee != "Toutes les années":
    elements_filtres = [
        element
        for element in elements_filtres
        if (
            (date_creation := convertir_date(
                element.get("date_creation")
            )) is not None
            and date_creation.year == annee_selectionnee
        )
    ]


# --------------------------------------------------
# Tri des succès
# --------------------------------------------------

if ordre_tri == "Date de création":

    elements = sorted(
        elements_filtres,
        key=lambda element: (
            convertir_date(element.get("date_creation")) is not None,
            convertir_date(element.get("date_creation")) or datetime.min,
        ),
        reverse=True,
    )

elif ordre_tri == "Date de validation":

    elements = sorted(
        elements_filtres,
        key=lambda element: (
            element.get("succes") is True,
            convertir_date(element.get("date_fin_validation")) is not None,
            convertir_date(element.get("date_fin_validation")) or datetime.min,
        ),
        reverse=True,
    )

else:  # Catégorie : ordre alphabétique

    elements = sorted(
        elements_filtres,
        key=lambda element: (
            str(element.get("categorie") or "Sans catégorie").strip().casefold(),
            str(element.get("nom") or "").casefold(),
        ),
    )



# --------------------------------------------------
# Style des cartes
# --------------------------------------------------

st.markdown(
    """
    <style>
    /* Cartes : hauteur fixe et fond sombre */

    div[class*="st-key-succes_"] {
        background-color: #202129 !important;
        border: none !important;
        border-radius: 14px !important;

        height: 340px !important;
        min-height: 340px !important;
        max-height: 340px !important;

        padding: 14px !important;
        margin-bottom: 12px;
        box-sizing: border-box;
        overflow: hidden;
    }

    /* Espacements à l'intérieur des cartes */

    div[class*="st-key-succes_"] [data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }

    /* Titre : 2 lignes maximum */

    .succes-titre {
        font-size: 16px;
        font-weight: 600;
        text-align: center;
        line-height: 24px;

        height: 48px;
        min-height: 48px;
        max-height: 48px;

        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 2;

        overflow: hidden;
        overflow-wrap: anywhere;
        word-break: break-word;

        margin: 0 0 8px 0;
    }

    /* Image : zone uniforme */

    div[class*="st-key-succes_"] [data-testid="stImage"] {
        height: 180px;
        min-height: 180px;
        max-height: 180px;
        width: 100%;
        overflow: hidden;
        border-radius: 8px;
        margin: 0;
    }

    div[class*="st-key-succes_"] [data-testid="stImage"] img {
        width: 100%;
        height: 180px;
        object-fit: contain;
    }

    /* Date : 2 lignes maximum */

    .succes-date {
        font-size: 13px;
        color: #b0b0b0;
        text-align: center;
        line-height: 16px;

        height: 40px;
        min-height: 40px;
        max-height: 40px;

        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 2;

        overflow: hidden;
        overflow-wrap: anywhere;
        word-break: break-word;

        margin-top: 8px;
        padding: 4px 0;
        box-sizing: border-box;
    }

    /* Image indisponible */

    .succes-image-absente {
        height: 180px;
        min-height: 180px;
        max-height: 180px;

        display: flex;
        align-items: center;
        justify-content: center;

        text-align: center;
        color: #b0b0b0;
        font-size: 13px;

        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Groupes d'affichage
# --------------------------------------------------

groupes = []

if ordre_tri == "Catégorie":

    categorie_actuelle = None
    groupe_actuel = []

    for element in elements:
        categorie = str(
            element.get("categorie") or "Sans catégorie"
        ).strip() or "Sans catégorie"

        if categorie != categorie_actuelle:
            if groupe_actuel:
                groupes.append((categorie_actuelle, groupe_actuel))

            categorie_actuelle = categorie
            groupe_actuel = []

        groupe_actuel.append(element)

    if groupe_actuel:
        groupes.append((categorie_actuelle, groupe_actuel))

elif ordre_tri == "Date de validation":

    valides = [
        element for element in elements
        if element.get("succes") is True
    ]

    non_valides = [
        element for element in elements
        if element.get("succes") is not True
    ]

    if valides:
        groupes.append(("Succès validés", valides))

    if non_valides:
        groupes.append(("Succès non validés", non_valides))

else:
    groupes.append((None, elements))


# --------------------------------------------------
# Affichage des succès : 6 colonnes maximum par ligne
# --------------------------------------------------

if not elements:
    st.info("Aucun succès à afficher pour cette année.")

else:
    for titre_groupe, elements_groupe in groupes:

        # Titre de groupe pour les tris par catégorie et validation
        if titre_groupe is not None:
            st.markdown(f"#### {html.escape(titre_groupe)}")

        # Chaque groupe démarre sur une nouvelle ligne
        for debut in range(0, len(elements_groupe), 6):

            elements_ligne = elements_groupe[debut:debut + 6]
            colonnes = st.columns(6, gap="medium")

            for index, (colonne, element) in enumerate(
                zip(colonnes, elements_ligne)
            ):

                with colonne:

                    if not isinstance(element, dict):
                        st.warning("Élément de succès invalide.")
                        continue

                    numero_carte = f"{titre_groupe}_{debut + index}"

                    with st.container(key=f"succes_{numero_carte}"):

                        # ----------------------------------
                        # Titre
                        # ----------------------------------

                        nom = html.escape(
                            str(element.get("nom") or "Sans titre")
                        )

                        st.markdown(
                            f'<div class="succes-titre">{nom}</div>',
                            unsafe_allow_html=True,
                        )

                        # ----------------------------------
                        # Recherche de l'image
                        # ----------------------------------

                        nom_image = element.get("image")

                        categorie = str(
                            element.get("categorie") or ""
                        ).strip().lower()

                        chemin_image = None

                        if isinstance(nom_image, str) and nom_image.strip():
                            image_candidate = (
                                DOSSIER_IMAGES / nom_image.strip()
                            )

                            try:
                                image_candidate.resolve().relative_to(
                                    DOSSIER_IMAGES.resolve()
                                )

                                if image_candidate.is_file():
                                    chemin_image = image_candidate

                            except (ValueError, OSError):
                                pass

                        if chemin_image is None:
                            image_defaut = IMAGES_DEFAUT.get(categorie)

                            if image_defaut:
                                image_candidate = (
                                    DOSSIER_IMAGES / image_defaut
                                )

                                if image_candidate.is_file():
                                    chemin_image = image_candidate

                        # ----------------------------------
                        # Affichage de l'image
                        # ----------------------------------

                        if chemin_image is not None:
                            st.image(
                                str(chemin_image),
                                use_container_width=True,
                            )
                        else:
                            st.markdown(
                                """
                                <div class="succes-image-absente">
                                    Image indisponible
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        # ----------------------------------
                        # Date et état du succès
                        # ----------------------------------

                        succes_obtenu = element.get("succes", False)

                        date_creation = afficher_date(
                            element.get("date_creation")
                        )
                        date_debut = afficher_date(
                            element.get("date_debut_validation")
                        )
                        date_fin = afficher_date(
                            element.get("date_fin_validation")
                        )

                        if succes_obtenu is True:
                            if date_debut and date_fin:
                                texte_date = (
                                    f"Déverrouillé du {date_debut} "
                                    f"au {date_fin}"
                                )
                            elif date_fin:
                                texte_date = f"Déverrouillé le {date_fin}"
                            elif date_debut:
                                texte_date = (
                                    f"Déverrouillé depuis le {date_debut}"
                                )
                            else:
                                texte_date = "Déverrouillé"
                        else:
                            texte_date = (
                                f"Créé le {date_creation}"
                                if date_creation
                                else "Date inconnue"
                            )

                        texte_date = html.escape(str(texte_date))

                        st.markdown(
                            f'<div class="succes-date">'
                            f'{texte_date}</div>',
                            unsafe_allow_html=True,
                        )

