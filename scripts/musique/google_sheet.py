import pandas as pd
import gspread
import streamlit as st
from google.oauth2.service_account import Credentials


SHEET_ID = "1V-U1cMxgZXxBW5N8M4hM_LPrsjn5HEv4oG63YerEmCc"


@st.cache_data(ttl=300)
def charger_musique():

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

    return pd.DataFrame(data)