
import gspread
import pandas as pd
import streamlit as st

from datetime import date
from google.oauth2.service_account import Credentials


SHEET_ID = "1EXdUL-iCTtOU-qBEyvKxN3qZzb2OMR4CdJ3RjddmERI"


# ==========================================================
# COLONNES DU GOOGLE SHEETS
# ==========================================================

COLUMNS = [
    "artiste",
    "titre",
    "choregraphe",
    "date_debut",
    "date_fin",
    "duree_apprentissage",
    "nombre_seance",
    "duree_seance",
    "style",
    "duree",
    "statut",
    "refaite",
    "date_fin_2",
    "date_fin_3",
    "date_fin_4"
]


# ==========================================================
# CONNEXION GOOGLE SHEETS
# ==========================================================

def get_sheet():

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ]
    )

    client = gspread.authorize(credentials)

    return client.open_by_key(SHEET_ID).sheet1


# ==========================================================
# CHARGEMENT DES DONNÉES
# ==========================================================

def load_danse_google_sheet():

    sheet = get_sheet()

    data = sheet.get_all_records()

    return pd.DataFrame(data)


# ==========================================================
# SAUVEGARDE COMPLÈTE DU TABLEAU
# ==========================================================

def save_danse_google_sheet(df):

    sheet = get_sheet()

    df = df.copy().fillna("")

    # Ajouter les colonnes manquantes
    for col in COLUMNS:

        if col not in df.columns:
            df[col] = ""

    # Respecter l'ordre des colonnes
    df = df.reindex(columns=COLUMNS)

    data = [
        df.columns.tolist()
    ] + df.values.tolist()

    sheet.clear()

    sheet.update(
        range_name="A1",
        values=data
    )


# ==========================================================
# AJOUT D'UNE NOUVELLE CHORÉGRAPHIE
# ==========================================================

def add_danse_google_sheet(
    artiste,
    titre,
    choregraphe,
    style,
    duree
):

    sheet = get_sheet()

    aujourd_hui = date.today().strftime("%Y-%m-%d")

    # Récupérer les colonnes présentes dans le Google Sheets
    headers = sheet.row_values(1)

    # Vérifier que toutes les colonnes nécessaires existent
    colonnes_manquantes = [
        col for col in COLUMNS
        if col not in headers
    ]

    if colonnes_manquantes:

        st.error(
            "Colonnes manquantes dans le Google Sheets : "
            + ", ".join(colonnes_manquantes)
        )

        return False

    # Préparer la nouvelle chorégraphie
    nouvelle_choregraphie = {
        "artiste": artiste,
        "titre": titre,
        "choregraphe": choregraphe,
        "date_debut": aujourd_hui,
        "date_fin": "",
        "duree_apprentissage": 0,
        "nombre_seance": 0,
        "duree_seance": 0,
        "style": style,
        "duree": duree,
        "statut": "en cours",
        "refaite": 0,
        "date_fin_2": "",
        "date_fin_3": "",
        "date_fin_4": ""
    }

    # Construire la ligne selon l'ordre réel des colonnes
    row = [
        nouvelle_choregraphie.get(col, "")
        for col in headers
    ]

    sheet.append_row(
        row,
        value_input_option="USER_ENTERED"
    )

    return True


# ==========================================================
# AJOUT DU TEMPS DE PRATIQUE
# ==========================================================

def add_practice_time(
    artiste,
    titre,
    temps
):

    sheet = get_sheet()

    # Vérifier la durée
    try:
        temps = float(temps)

    except (ValueError, TypeError):

        st.error("La durée de pratique est invalide.")

        return False

    if temps <= 0:

        st.error("La durée de pratique doit être supérieure à 0.")

        return False

    # Récupération des en-têtes et des données
    headers = sheet.row_values(1)

    records = sheet.get_all_records()

    # Associer chaque colonne à son numéro
    colonnes = {
        nom: index + 1
        for index, nom in enumerate(headers)
    }

    # Vérifier les colonnes nécessaires
    colonnes_requises = [
        "artiste",
        "titre",
        "duree_apprentissage",
        "nombre_seance",
        "duree_seance",
        "refaite",
        "date_fin",
        "date_fin_2",
        "date_fin_3",
        "date_fin_4"
    ]

    colonnes_manquantes = [
        col for col in colonnes_requises
        if col not in colonnes
    ]

    if colonnes_manquantes:

        st.error(
            "Colonnes manquantes dans le Google Sheets : "
            + ", ".join(colonnes_manquantes)
        )

        return False

    # Rechercher la chorégraphie
    for index, row in enumerate(records, start=2):

        if (
            str(row.get("artiste", "")).strip() == str(artiste).strip()
            and
            str(row.get("titre", "")).strip() == str(titre).strip()
        ):

            try:

                # Valeurs actuelles
                ancienne_duree = float(
                    row.get("duree_apprentissage", 0) or 0
                )

                ancien_nb = int(
                    row.get("nombre_seance", 0) or 0
                )

                refaite = int(
                    row.get("refaite", 0) or 0
                )

            except (ValueError, TypeError):

                st.error(
                    "Une valeur numérique de la chorégraphie est invalide."
                )

                return False

            # Déterminer la date de fin à mettre à jour
            colonnes_dates = {
                0: "date_fin",
                1: "date_fin_2",
                2: "date_fin_3",
                3: "date_fin_4"
            }

            if refaite not in colonnes_dates:

                st.error(
                    "La valeur de 'refaite' doit être comprise entre 0 et 3."
                )

                return False

            colonne_date = colonnes_dates[refaite]

            # Calcul des nouvelles valeurs
            nouvelle_duree = ancienne_duree + temps

            nouveau_nb = ancien_nb + 1

            nouvelle_moyenne = round(
                nouvelle_duree / nouveau_nb,
                1
            )

            aujourd_hui = date.today().strftime("%Y-%m-%d")

            # Mise à jour des cellules
            updates = [
                {
                    "range": (
                        f"{gspread.utils.rowcol_to_a1(index, colonnes[colonne_date])}"
                    ),
                    "values": [[aujourd_hui]]
                },
                {
                    "range": (
                        f"{gspread.utils.rowcol_to_a1(index, colonnes['duree_apprentissage'])}"
                    ),
                    "values": [[nouvelle_duree]]
                },
                {
                    "range": (
                        f"{gspread.utils.rowcol_to_a1(index, colonnes['nombre_seance'])}"
                    ),
                    "values": [[nouveau_nb]]
                },
                {
                    "range": (
                        f"{gspread.utils.rowcol_to_a1(index, colonnes['duree_seance'])}"
                    ),
                    "values": [[nouvelle_moyenne]]
                }
            ]

            sheet.batch_update(
                updates,
                value_input_option="USER_ENTERED"
            )

            return True

    st.error(
        f"Chorégraphie introuvable : {artiste} - {titre}"
    )

    return False
