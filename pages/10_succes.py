import json
import html
from pathlib import Path
from datetime import date, datetime

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
# Compteur d'étoiles acquises
# --------------------------------------------------

total_etoiles = sum(
    int(element.get("etoiles", 0) or 0)
    for element in elements
    if isinstance(element, dict)
    and element.get("succes") is True
)

st.markdown(
    f"### ⭐ Nombre d'étoiles acquises : {total_etoiles}"
)

# --------------------------------------------------
# Choix de l'ordre d'affichage
# --------------------------------------------------

ordre_tri = st.radio(
    "Trier les succès par :",
    options=[
        "Date de création",
        "Date de fin de validation",
    ],
    horizontal=True,
)

```python
def convertir_date(valeur):
    """Convertit une date en clé de tri, en acceptant les dates ISO."""
    if not valeur:
        return None

    try:
        # Prend en charge YYYY-MM-DD et les dates avec heure.
        resultat = datetime.fromisoformat(
            str(valeur).strip().replace("Z", "+00:00")
        )

        # Uniformise les dates avec ou sans fuseau horaire.
        if resultat.tzinfo is not None:
            resultat = resultat.replace(tzinfo=None)

        return resultat

    except (ValueError, TypeError):
        return None


if ordre_tri == "Date de création":
    elements = sorted(
        elements,
        key=lambda element: (
            convertir_date(element.get("date_creation"))
            if isinstance(element, dict)
            else None
        ) or datetime.min,
        reverse=True,
    )

else:
    # Les éléments avec une date de fin passent en premier.
    # La date_fin_validation la plus récente apparaît en haut.
    # Les éléments sans date de fin restent tout en bas.
    elements = sorted(
        elements,
        key=lambda element: (
            convertir_date(element.get("date_fin_validation"))
            if isinstance(element, dict)
            else None
        ) or datetime.min,
        reverse=True,
    )

    # Déplace explicitement en bas les éléments sans date de fin.
    elements = [
        element for element in elements
        if isinstance(element, dict)
        and convertir_date(element.get("date_fin_validation")) is not None
    ] + [
        element for element in elements
        if not isinstance(element, dict)
        or convertir_date(element.get("date_fin_validation")) is None
    ]
```
# --------------------------------------------------
# Style des cartes
# --------------------------------------------------

st.markdown(
    """
    <style>
    /* ------------------------------------------
       Cartes : hauteur fixe et fond sombre
       ------------------------------------------ */

    div[class*="st-key-succes_"] {
        background-color: #262626 !important;
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

    /* Évite les espacements imprévus à l'intérieur */
    div[class*="st-key-succes_"] [data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }

    /* ------------------------------------------
       Titre : 2 lignes maximum
       ------------------------------------------ */

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

    /* ------------------------------------------
       Image : zone uniforme
       ------------------------------------------ */

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

    /* ------------------------------------------
       Date : 2 lignes maximum
       ------------------------------------------ */

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

    /* ------------------------------------------
       Image indisponible
       ------------------------------------------ */

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

                # Ignore les entrées JSON incorrectes
                if not isinstance(element, dict):
                    st.warning("Élément de succès invalide.")
                    continue

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
