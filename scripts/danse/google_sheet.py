import gspread
import pandas as pd
import streamlit as st

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

    records = sheet.get_all_records()

    for index, row in enumerate(records, start=2):

        if (
            row["artiste"] == artiste
            and row["titre"] == titre
        ):

            ancienne_duree = float(
                row.get(
                    "duree_apprentissage",
                    0
                ) or 0
            )

            ancien_nb = int(
                row.get(
                    "nombre_seance",
                    0
                ) or 0
            )

            nouvelle_duree = (
                ancienne_duree + temps
            )

            nouveau_nb = (
                ancien_nb + 1
            )

            nouvelle_moyenne = round(
                nouvelle_duree / nouveau_nb,
                1
            )

            aujourd_hui = pd.Timestamp.today().strftime(
                "%Y-%m-%d"
            )

            # date_fin
            sheet.update_cell(
                index,
                5,
                aujourd_hui
            )

            # duree_apprentissage
            sheet.update_cell(
                index,
                6,
                nouvelle_duree
            )

            # nombre_seance
            sheet.update_cell(
                index,
                7,
                nouveau_nb
            )

            # duree_seance
            sheet.update_cell(
                index,
                8,
                nouvelle_moyenne
            )

            return True

    return False