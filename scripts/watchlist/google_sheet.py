import gspread
import streamlit as st

from google.oauth2.service_account import Credentials


SHEET_ID = (
    "1r-cWFbD68vRs3FNTeI3w11Dq--ZeucvMvRKbrq9k24A"
)



def save_movies_google_sheet(df):


    credentials = Credentials.from_service_account_info(

        st.secrets["gcp_service_account"],

        scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ]

    )


    client = gspread.authorize(
        credentials
    )


    sheet = client.open_by_key(
        SHEET_ID
    ).sheet1



    sheet.clear()


    data = [
        df.columns.tolist()
    ] + df.values.tolist()



    sheet.update(
        data
    )