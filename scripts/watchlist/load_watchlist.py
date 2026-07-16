import pandas as pd
import gspread
import streamlit as st

from google.oauth2.service_account import Credentials

SHEET_ID = "1r-cWFbD68vRs3FNTeI3w11Dq--ZeucvMvRKbrq9k24A"


def load_movies_google_sheet():

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ]
    )

    client = gspread.authorize(credentials)

    sheet = client.open_by_key(SHEET_ID).sheet1

    data = sheet.get_all_records()

    movies = pd.DataFrame(data)


    # Conversion des dates
    movies["watched_at"] = pd.to_datetime(
        movies["watched_at"],
        errors="coerce"
    )


    # Conversion des nombres
    movies["rating"] = pd.to_numeric(
        movies["rating"],
        errors="coerce"
    )

    movies["tmdb_rating"] = pd.to_numeric(
        movies["tmdb_rating"],
        errors="coerce"
    )


    return movies


def load_series_google_sheet():

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ]
    )

    client = gspread.authorize(credentials)

    sheet = (
        client.open_by_key(SHEET_ID)
        .worksheet("series")
    )

    data = sheet.get_all_records()

    series = pd.DataFrame(data)

    for col in ["first_seen", "last_watch"]:
        if col in series.columns:
            series[col] = pd.to_datetime(
                series[col],
                errors="coerce"
            )

    for col in ["episodes", "progress", "score"]:
        if col in series.columns:
            series[col] = pd.to_numeric(
                series[col],
                errors="coerce"
            )

    return series