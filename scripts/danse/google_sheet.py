import gspread
import streamlit as st

from google.oauth2.service_account import Credentials


SHEET_ID = "1EXdUL-iCTtOU-qBEyvKxN3qZzb2OMR4CdJ3RjddmERI"


def save_danse_google_sheet(df):

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


    df = df.copy()


    # Remplacement valeurs vides
    df = df.fillna("")


    # Renommage pour correspondre au Google Sheet
    df = df.rename(
        columns={
            "Style": "style",
            "Durée (s)": "duree",
            "Difficultée": "difficulte",
            "Estimation": "estimation",
            "Note": "note"
        }
    )


    # Ajout statut si absent
    if "statut" not in df.columns:
        df["statut"] = ""


    columns = [
        "artiste",
        "titre",
        "choregraphe",
        "duree_apprentissage",
        "style",
        "duree",
        "difficulte",
        "estimation",
        "note",
        "statut"
    ]


    df = df.reindex(
        columns=columns
    )


    # Conversion dataframe vers liste Google Sheet
    data = [
        df.columns.tolist()
    ] + df.values.tolist()


    # Nettoyage puis écriture
    sheet.clear()

    sheet.update(
        data
    )