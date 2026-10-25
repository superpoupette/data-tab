import gspread
import pandas as pd
import streamlit as st
from datetime import date

from google.oauth2.service_account import Credentials


SHEET_ID = "1EXdUL-iCTtOU-qBEyvKxN3qZzb2OMR4CdJ3RjddmERI"


def get_sheet():

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ]
    )

    client = gspread.authorize(credentials)

    return client.open_by_key(
        SHEET_ID
    ).sheet1


def save_danse_google_sheet(df):

    sheet = get_sheet()

    df = df.copy().fillna("")

    columns = [
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
        "difficulte",
        "estimation",
        "note",
        "statut"
    ]

    for col in columns:
        if col not in df.columns:
            df[col] = ""

    df = df.reindex(columns=columns)

    data = [
        df.columns.tolist()
    ] + df.values.tolist()

    sheet.clear()

    sheet.update(data)


def load_danse_google_sheet():

    sheet = get_sheet()

    data = sheet.get_all_records()

    return pd.DataFrame(data)


def add_danse_google_sheet(
    artiste,
    titre,
    choregraphe,
    style,
    duree
    ):

    sheet = get_sheet()

    aujourd_hui = date.today().strftime("%Y-%m-%d")

    row = [
        artiste,          # artiste
        titre,            # titre
        choregraphe,      # choregraphe
        aujourd_hui,      # date_debut
        "",               # date_fin
        0,                # duree_apprentissage
        0,                # nombre_seance
        0,                # duree_seance
        style,            # style
        duree,            # duree
        "",               # difficulte
        "",               # estimation
        "",               # note
        "en cours"        # statut
    ]

    sheet.append_row(row)


def add_practice_time(
    artiste,
    titre,
    temps
):
    sheet = get_sheet()

    # Récupération des en-têtes et des données
    headers = sheet.row_values(1)
    records = sheet.get_all_records()

    # Associer chaque nom de colonne à son numéro
    colonnes = {
        nom: index + 1
        for index, nom in enumerate(headers)
    }

    for index, row in enumerate(records, start=2):

        if (
            row["artiste"] == artiste
            and row["titre"] == titre
        ):

            # Récupération des valeurs actuelles
            ancienne_duree = float(
                row.get("duree_apprentissage", 0) or 0
            )

            ancien_nb = int(
                row.get("nombre_seance", 0) or 0
            )

            # Calcul des nouvelles valeurs
            nouvelle_duree = ancienne_duree + temps
            nouveau_nb = ancien_nb + 1

            nouvelle_moyenne = round(
                nouvelle_duree / nouveau_nb,
                1
            )

            # Date actuelle
            aujourd_hui = pd.Timestamp.today().strftime(
                "%Y-%m-%d"
            )

            # Détermination de la colonne de date
            refaite = str(
                row.get("refaite", "")
            ).strip()

            if refaite == "" or refaite == "0":
                colonne_date = "date_fin"

            elif refaite == "1":
                colonne_date = "date_fin_2"

            elif refaite == "2":
                colonne_date = "date_fin_3"

            else:
                colonne_date = None

            # Mise à jour de la date si la valeur est reconnue
            if colonne_date is not None:

                if colonne_date in colonnes:

                    sheet.update_cell(
                        index,
                        colonnes[colonne_date],
                        aujourd_hui
                    )

                else:
                    st.error(
                        f"La colonne '{colonne_date}' "
                        "est absente du Google Sheets."
                    )
                    return False

            # Mise à jour du temps total d'apprentissage
            sheet.update_cell(
                index,
                colonnes["duree_apprentissage"],
                nouvelle_duree
            )

            # Mise à jour du nombre de séances
            sheet.update_cell(
                index,
                colonnes["nombre_seance"],
                nouveau_nb
            )

            # Mise à jour de la durée moyenne par séance
            sheet.update_cell(
                index,
                colonnes["duree_seance"],
                nouvelle_moyenne
            )

            return True

    return False