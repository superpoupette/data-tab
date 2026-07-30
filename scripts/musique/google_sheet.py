import pandas as pd
import gspread
import streamlit as st
from google.oauth2.service_account import Credentials


MUSIC_SHEET_ID = "1V-U1cMxgZXxBW5N8M4hM_LPrsjn5HEv4oG63YerEmCc"


def get_music_sheet():

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ]
    )

    client = gspread.authorize(credentials)

    return client.open_by_key(
        MUSIC_SHEET_ID
    ).sheet1



def charger_albums():

    sheet = get_music_sheet()

    data = sheet.get_all_records()

    return pd.DataFrame(data)


import pandas as pd
import gspread
import streamlit as st
from google.oauth2.service_account import Credentials


SHEET_ID = "1V-U1cMxgZXxBW5N8M4hM_LPrsjn5HEv4oG63YerEmCc"


def get_music_sheet():

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



def charger_musique():

    sheet = get_music_sheet()

    data = sheet.get_all_records()

    df = pd.DataFrame(data)

    return df