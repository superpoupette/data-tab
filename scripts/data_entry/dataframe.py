import pandas as pd
import os
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

CSV_FILE = "today_data.csv"


def create_today_dataframe():

    columns = [
        "date",
        "best_moment",
        "people_seen",
        "people_work",
        "sommeil"
    ]

    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)

        # Au cas où le CSV contient encore les anciennes colonnes
        df = df[columns]

    else:
        df = pd.DataFrame(columns=columns)
        df.to_csv(
            CSV_FILE,
            index=False,
            encoding="utf-8-sig"
        )

    return df


def add_today_entry(
    df,
    today_date,
    best_moment,
    people_seen,
    people_work,
    sommeil
):

    # La date existe déjà
    if today_date in df["date"].astype(str).values:

        idx = df.index[df["date"].astype(str) == today_date][0]

        if best_moment != "":
            df.at[idx, "best_moment"] = best_moment

        if people_seen != "":
            df.at[idx, "people_seen"] = people_seen

        # Toujours mettre à jour la case Travail
        df.at[idx, "people_work"] = people_work

        if sommeil is not None:
            df.at[idx, "sommeil"] = sommeil

    # Nouvelle date
    else:

        new_row = pd.DataFrame([{
            "date": today_date,
            "best_moment": best_moment,
            "people_seen": people_seen,
            "people_work": people_work,
            "sommeil": sommeil
        }])

        df = pd.concat(
            [df, new_row],
            ignore_index=True
        )

    return df


def save_dataframe_csv(df):

    df.to_csv(
        CSV_FILE,
        index=False,
        encoding="utf-8-sig"
    )


def save_to_google_sheet(row):

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ]
    )

    client = gspread.authorize(credentials)

    sheet = client.open_by_key(
        "1AZ-DudhWGHJP6-A5mXDsPgoYIgUvZL5YsVbTaK5eeMk"
    ).sheet1

    sheet.append_row(row)