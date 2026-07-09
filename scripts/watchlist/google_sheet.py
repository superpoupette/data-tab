import pandas as pd
import gspread
import streamlit as st

from google.oauth2.service_account import Credentials


SHEET_ID = "1r-cWFbD68vRs3FNTeI3w11Dq--ZeucvMvRKbrq9k24A"


def save_movies_google_sheet(df):

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    client = gspread.authorize(credentials)

    sheet = client.open_by_key(SHEET_ID).sheet1

    df = df.copy()

    # Conversion de chaque cellule en type compatible Google Sheets
    def convert_value(value):

        if pd.isna(value):
            return ""

        if isinstance(value, pd.Timestamp):
            return value.strftime("%Y-%m-%d")

        if hasattr(value, "item"):
            return value.item()

        return value

    values = [
        [convert_value(v) for v in row]
        for row in df.itertuples(index=False, name=None)
    ]

    sheet.clear()

    sheet.update(
        [df.columns.tolist()] + values
    )