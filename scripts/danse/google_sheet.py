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

    sheet = client.open_by_key(
        SHEET_ID
    ).sheet1

    return sheet



def save_danse_google_sheet(df):

    sheet = get_sheet()

    df = df.copy()

    df = df.fillna("")


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


    df = df.reindex(
        columns=columns
    )


    data = [
        df.columns.tolist()
    ] + df.values.tolist()


    sheet.clear()

    sheet.update(
        data
    )



def load_danse_google_sheet():

    sheet = get_sheet()

    data = sheet.get_all_records()

    df = pd.DataFrame(
        data
    )

    return df


import gspread
import streamlit as st

from google.oauth2.service_account import Credentials


SHEET_ID = "1EXdUL-iCTtOU-qBEyvKxN3qZzb2OMR4CdJ3RjddmERI"


def get_danse_sheet():

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



def add_danse_google_sheet(
    artiste,
    titre,
    choregraphe,
    duree
):

    sheet = get_danse_sheet()


    row = [
        artiste,
        titre,
        choregraphe,
        "",              # date_debut
        "",              # date_fin
        0,               # duree_apprentissage
        0,               # nombre_seance
        0,               # duree_seance
        "",              # style
        duree,           # duree
        "",              # difficulte
        "",              # estimation
        "",              # note
        "en cours"       # statut
    ]


    sheet.append_row(row)


    def get_danse_sheet():

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



def load_danse_google_sheet():

    sheet = get_danse_sheet()

    data = sheet.get_all_records()

    df = pd.DataFrame(data)

    return df



def add_practice_time(
    artiste,
    titre,
    temps
):

    sheet = get_danse_sheet()

    records = sheet.get_all_records()


    for index, row in enumerate(records, start=2):

        if (
            row["artiste"] == artiste
            and row["titre"] == titre
        ):

            ancienne_duree = float(
                row["duree_apprentissage"]
                or 0
            )

            nouvelle_duree = (
                ancienne_duree
                + temps
            )


            sheet.update_cell(
                index,
                6,   # colonne duree_apprentissage
                nouvelle_duree
            )


            return True


    return False