import pandas as pd
import gspread
import streamlit as st

from google.oauth2.service_account import Credentials

SHEET_ID = "1r-cWFbD68vRs3FNTeI3w11Dq--ZeucvMvRKbrq9k24A"


# ==========================
# OUTILS DE CONVERSION
# ==========================

def convertir_nombre(colonne):
    valeurs = (
        colonne
        .astype("string")
        .str.strip()
        .str.replace("\u00a0", "", regex=False)  # Espaces insécables
        .str.replace(" ", "", regex=False)       # Espaces classiques
        .replace("", pd.NA)
    )

    # Accepte aussi bien 3,5 que 3.5
    valeurs = valeurs.str.replace(",", ".", regex=False)

    return pd.to_numeric(valeurs, errors="coerce")


def charger_client_google_sheets():

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ]
    )

    return gspread.authorize(credentials)


# ==========================
# CHARGEMENT DES FILMS
# ==========================

def load_movies_google_sheet():

    client = charger_client_google_sheets()

    sheet = (
        client
        .open_by_key(SHEET_ID)
        .worksheet("movies")
    )

    data = sheet.get_all_records()

    movies = pd.DataFrame(data)

    # --------------------------
    # Conversion des dates
    # --------------------------

    if "watched_at" in movies.columns:
        movies["watched_at"] = pd.to_datetime(
            movies["watched_at"],
            errors="coerce"
        )

    # --------------------------
    # Conversion des nombres
    # --------------------------

    for col in ["rating", "tmdb_rating"]:
        if col in movies.columns:
            movies[col] = convertir_nombre(movies[col])

    return movies


# ==========================
# CHARGEMENT DES SÉRIES / ANIMÉS
# ==========================

def load_series_google_sheet():

    client = charger_client_google_sheets()

    sheet = (
        client
        .open_by_key(SHEET_ID)
        .worksheet("series")
    )

    data = sheet.get_all_records()

    series = pd.DataFrame(data)

    # --------------------------
    # Conversion des dates
    # --------------------------

    for col in ["first_seen", "last_watch"]:
        if col in series.columns:
            series[col] = pd.to_datetime(
                series[col],
                errors="coerce"
            )

    # --------------------------
    # Conversion des nombres
    # --------------------------

    for col in ["episodes", "progress", "score"]:
        if col in series.columns:
            series[col] = convertir_nombre(series[col])

    return series
