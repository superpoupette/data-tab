print(">>> google_sheet.py chargé")

import pandas as pd
import gspread
import streamlit as st

from google.oauth2.service_account import Credentials


SHEET_ID = "1r-cWFbD68vRs3FNTeI3w11Dq--ZeucvMvRKbrq9k24A"


def get_google_sheet():

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ]
    )

    client = gspread.authorize(
        credentials
    )

    return client.open_by_key(
        SHEET_ID
    )


def get_worksheet(sheet_name):

    spreadsheet = get_google_sheet()

    try:

        sheet = spreadsheet.worksheet(
            sheet_name
        )

    except gspread.exceptions.WorksheetNotFound:

        sheet = spreadsheet.add_worksheet(
            title=sheet_name,
            rows="1000",
            cols="30"
        )

    return sheet



def convert_value(value):

    if pd.isna(value):
        return ""

    if isinstance(value, pd.Timestamp):
        return value.strftime(
            "%Y-%m-%d"
        )

    if hasattr(value, "item"):
        return value.item()

    return value



def save_google_sheet(
    df,
    sheet_name
):

    sheet = get_worksheet(
        sheet_name
    )

    df = df.copy()


    values = [
        df.columns.tolist()
    ] + [
        [
            convert_value(v)
            for v in row
        ]
        for row in df.itertuples(
            index=False,
            name=None
        )
    ]


    sheet.clear()

    sheet.update(
        range_name="A1",
        values=values
    )



def load_google_sheet(
    sheet_name
):

    sheet = get_worksheet(
        sheet_name
    )


    data = sheet.get_all_records()


    df = pd.DataFrame(
        data
    )


    return df

def add_movie_google_sheet(
    movie,
    watched_at,
    rating
):

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ]
    )

    client = gspread.authorize(credentials)

    sheet = (
        client.open_by_key(SHEET_ID)
        .worksheet("movies")
    )

    row = [
        str(movie.get("tvdb_id", "")),
        str(movie.get("imdb_id", "")),
        str(movie.get("title", "")),
        str(movie.get("year", "")),
        str(movie.get("director", "")),
        watched_at,
        rating,
        "movie",
        "watched",
        str(movie.get("style", "")),
        str(movie.get("country", "")),
        str(movie.get("overview", "")),
        movie.get("poster_path", ""),
        movie.get("tmdb_rating", "")
    ]

    sheet.append_row(
        row,
        value_input_option="USER_ENTERED"
    )


print(">>> fin du fichier")