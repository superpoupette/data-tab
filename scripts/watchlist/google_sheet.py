import gspread
import streamlit as st

from google.oauth2.service_account import Credentials


SHEET_ID = (
    "1r-cWFbD68vRs3FNTeI3w11Dq--ZeucvMvRKbrq9k24A"
)



def save_movies_google_sheet(df):

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    client = gspread.authorize(credentials)

    sheet = client.open_by_key(SHEET_ID).sheet1

    df = df.copy()

    # Conversion des dates
    for col in df.select_dtypes(include=["datetime64[ns]"]).columns:
        df[col] = df[col].dt.strftime("%Y-%m-%d")

    # Remplacement des NaN
    df = df.fillna("")

    # Effacer uniquement le contenu
    sheet.clear()

    # Réécrire les en-têtes + les données
    sheet.update([df.columns.tolist()] + df.values.tolist())