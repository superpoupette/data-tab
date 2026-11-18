import gspread
import pandas as pd
import streamlit as st

# ==========================
# CONFIGURATION
# ==========================

st.set_page_config(
    page_title="Culture",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Wikicollection")

# --------------------------------------------------
# Configuration Google Sheets
# --------------------------------------------------

SHEET_ID = "11_RcYunE4kKJmF1Jo6g1MfoAy3di-S0j7BFDHWTdPh0"


@st.cache_resource
def get_sheet():

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ]
    )

    client = gspread.authorize(credentials)

    return client.open_by_key(SHEET_ID).sheet1


@st.cache_data(ttl=300)
def load_succes_google_sheet():

    sheet = get_sheet()

    data = sheet.get_all_records()

    return pd.DataFrame(data)



st.dataframe(
    data,
    use_container_width=True
)
