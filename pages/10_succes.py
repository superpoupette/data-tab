import json
import html
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
        f"Le fichier succes.json est introuvable : {FICHIER_JSON}"
    )
    st.stop()

try:
    with open(FICHIER_JSON, "r", encoding="utf-8") as fichier:
        elements = json.load(fichier)

except json.JSONDecodeError as erreur:
    st.error(f"Erreur dans le fichier succes.json : {erreur}")
    st.stop()

except OSError as erreur:
    st.error(f"Impossible de lire succes.json : {erreur}")
    st.stop()


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
    /* Fond de chaque carte */
    div[class*="st-key-succes_"] {
        background-color: #262626 !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 14px 14px 22px 14px !important;
        margin-bottom: 12px;
        box-sizing: border-box;
    }

    /* Supprime les éventuels contours des éléments internes */
    div[class*="st-key-succes_"] [data-testid="stImage"] {
        border-radius: 8px;
        overflow: hidden;
    }

    /* Titre */
    .succes-titre {
        font-size: 16px;
        font-weight: 600;
        text-align: center;
        min-height: 55px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow-wrap: anywhere;
        word-break: break-word;
        margin-bottom: 12px;
    }

    /* Date */
    .succes-date {
        font-size: 13px;
        color: #b0b0b0;
        text-align: center;
        margin-top: 18px;
        padding: 8px 0 4px 0;
    }

    /* Message si aucune image n'est disponible */
    .succes-image-absente {
        min-height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: #b0b0b0;
        font-size: 13px;
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

        for index, (colonne, element) in enumerate(
            zip(colonnes, elements_ligne)
        ):

            with colonne:

                # Le fond est appliqué à ce conteneur
                numero_carte = debut + index

                with st.container(key=f"succes_{numero_carte}"):

                    # ------------------------------------------
                    # Titre
                    # ------------------------------------------

                    nom = html.escape(
                        str(element.get("nom") or "Sans titre")
                    )

                    st.markdown(
                        f'<div class="succes-titre">{nom}</div>',
                        unsafe_allow_html=True,
                    )

                    # ------------------------------------------
                    # Recherche de l'image
                    # ------------------------------------------

                    nom_image = element.get("image")
                    categorie = str(
                        element.get("categorie") or ""
                    ).strip().lower()

                    chemin_image = None

                    # Image spécifique
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

                    # Image par défaut selon la catégorie
                    if chemin_image is None:

                        image_defaut = IMAGES_DEFAUT.get(categorie)

                        if image_defaut:
                            image_candidate = (
                                DOSSIER_IMAGES / image_defaut
                            )

                            if image_candidate.is_file():
                                chemin_image = image_candidate

                    # ------------------------------------------
                    # Affichage de l'image
                    # ------------------------------------------

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


                    # ------------------------------------------
                    # Texte sous l'image selon l'état du succès
                    # ------------------------------------------

                    succes_obtenu = element.get("succes", False)

                    date_creation = element.get("date_creation")
                    date_debut = element.get("date_debut_validation")
                    date_fin = element.get("date_fin_validation")

                    if succes_obtenu is True:
                        if date_debut and date_fin:
                            texte_date = (
                                f"Déverrouillé de {date_debut} à {date_fin}"
                            )
                        elif date_fin:
                            texte_date = f"Déverrouillé le {date_fin}"
                        elif date_debut:
                            texte_date = f"Déverrouillé depuis le {date_debut}"
                        else:
                            texte_date = "Déverrouillé"

                    else:
                        texte_date = f"Créé en {date_creation}" if date_creation else "Date inconnue"

                    texte_date = html.escape(str(texte_date))

                    st.markdown(
                        f'<div class="succes-date">{texte_date}</div>',
                        unsafe_allow_html=True,
                    )

