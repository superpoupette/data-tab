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

    # Remplacement des valeurs manquantes
    df = df.fillna("")

    # Compatibilité avec les anciens noms de colonnes
    df = df.rename(
        columns={
            "Style": "style",
            "Duree (s)": "duree",
            "Difficulte": "difficulte",
            "Estimation": "estimation",
            "Note": "note",
        }
    )

    # Ajout de la colonne statut si absente
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

    df = df.reindex(columns=columns)

    # Conversion en liste pour Google Sheets
    data = [df.columns.tolist()] + df.values.tolist()

    # Remplacement complet du contenu
    sheet.clear()
    sheet.update(data)