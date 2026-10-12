
import json
from pathlib import Path

import streamlit as st


# --------------------------------------------------
# Configuration de la page
# --------------------------------------------------

st.set_page_config(
    page_title="Mes succès",
    page_icon="🏆",
    layout="wide",
)

st.title("Mes succès")


# --------------------------------------------------
# Chemins des fichiers
# --------------------------------------------------

# Le fichier actuel est dans pages/
# Le dossier parent correspond à la racine du projet.
BASE_DIR = Path(__file__).resolve().parent.parent

FICHIER_JSON = BASE_DIR / "succes.json"
DOSSIER_IMAGES = BASE_DIR / "images" / "succes"


# --------------------------------------------------
# Images par défaut selon la catégorie
# --------------------------------------------------

IMAGES_DEFAUT = {
    "sport": "sport.png",
    "dessin": "dessin.png",
    "danse": "danse.png",
    "creatif": "creatif.png",
}


# --------------------------------------------------
# Chargement des données JSON
# --------------------------------------------------

if not FICHIER_JSON.is_file():
    st.error(
        f"Le fichier succes.json est introuvable : "
        f"{FICHIER_JSON}"
    )
    st.stop()

try:
    with open(FICHIER_JSON, "r", encoding="utf-8") as fichier:
        elements = json.load(fichier)

except json.JSONDecodeError as erreur:
    st.error(
        f"Le fichier succes.json contient une erreur JSON : "
        f"{erreur}"
    )
    st.stop()

except OSError as erreur:
    st.error(
        f"Impossible de lire le fichier succes.json : "
        f"{erreur}"
    )
    st.stop()


# Vérification du contenu
if not isinstance(elements, list):
    st.error(
        "Le fichier succes.json doit contenir "
        "une liste d'éléments entre crochets []."
    )
    st.stop()


# --------------------------------------------------
# Style des cartes
# --------------------------------------------------

st.markdown(
    """
    <style>
    .succes-carte {
        background-color: #262626;
        border-radius: 14px;
        padding: 14px;
        height: 100%;
    }

    .succes-titre {
        font-size: 16px;
        font-weight: 600;
        text-align: center;
        min-height: 55px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow-wrap: anywhere;
        margin-bottom: 12px;
    }

    .succes-date {
        font-size: 13px;
        color: #b0b0b0;
        text-align: center;
        margin-top: 18px;
        padding: 8px 0 4px 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Affichage des succès : 6 colonnes par ligne
# --------------------------------------------------

if not elements:
    st.info("Aucun succès à afficher.")

else:
    for debut in range(0, len(elements), 6):

        elements_ligne = elements[debut:debut + 6]
        colonnes = st.columns(6, gap="medium")

        for colonne, element in zip(colonnes, elements_ligne):

            with colonne:

                # Fond personnalisé sans contour
                st.markdown(
                    '<div class="succes-carte">',
                    unsafe_allow_html=True,
                )

                # Titre
                nom = element.get("nom", "Sans titre")

                st.markdown(
                    f'<div class="succes-titre">'
                    f'{nom}</div>',
                    unsafe_allow_html=True,
                )

                # Image spécifique ou image par défaut
                nom_image = element.get("image")
                categorie = element.get("categorie", "").lower()

                chemin_image = None

                if nom_image:
                    image_candidate = DOSSIER_IMAGES / nom_image

                    try:
                        image_candidate.resolve().relative_to(
                            DOSSIER_IMAGES.resolve()
                        )

                        if image_candidate.is_file():
                            chemin_image = image_candidate

                    except ValueError:
                        pass

                if chemin_image is None:
                    image_defaut = IMAGES_DEFAUT.get(categorie)

                    if image_defaut:
                        image_candidate = (
                            DOSSIER_IMAGES / image_defaut
                        )

                        if image_candidate.is_file():
                            chemin_image = image_candidate

                if chemin_image is not None:
                    st.image(
                        str(chemin_image),
                        use_container_width=True,
                    )
                else:
                    st.info("Image indisponible")

                # Date avec un espace en dessous de l'image
                date_creation = element.get(
                    "date_creation"
                ) or "Date inconnue"

                st.markdown(
                    f'<div class="succes-date">'
                    f'{date_creation}</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True,
                )

