import gspread
import pandas as pd
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


    # Remplacement des valeurs manquantes
    df = df.fillna("")


    # Compatibilité anciens noms de colonnes
    df = df.rename(
        columns={
            "Style": "style",
            "Durée (s)": "duree",
            "Difficultée": "difficulte",
            "Estimation": "estimation",
            "Note": "note"
        }
    )


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


    # Ajoute les colonnes manquantes
    for col in columns:
        if col not in df.columns:
            df[col] = ""


    # Réorganisation finale
    df = df.reindex(
        columns=columns
    )


    # Conversion dataframe vers Google Sheet
    data = [
        df.columns.tolist()
    ] + df.values.tolist()


    # Réécriture complète
    sheet.clear()

    sheet.update(
        data
    )


    def load_danse_google_sheet():

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


    data = sheet.get_all_records()


    df = pd.DataFrame(data)


    return df