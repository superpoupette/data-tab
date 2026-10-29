import pandas as pd
import gspread
import streamlit as st

from google.oauth2.service_account import Credentials


SHEET_ID = "1r-cWFbD68vRs3FNTeI3w11Dq--ZeucvMvRKbrq9k24A"


# ==========================
# OUTILS DE CONVERSION
# ==========================

def convertir_nombre(colonne):
    """
    Convertit les nombres en acceptant la virgule ou le point décimal.
    Exemples : '3,5' -> 3.5 ; '3.5' -> 3.5 ; '10' -> 10.0
    """

    valeurs = (
        colonne.astype("string")
        .str.strip()
        .str.replace("\u00a0", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
        .replace("", pd.NA)
    )

    return pd.to_numeric(valeurs, errors="coerce")


def charger_client_google_sheets():
    """Connecte le client à Google Sheets."""

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ]
    )

    return gspread.authorize(credentials)


def charger_feuille_en_dataframe(sheet):
    """
    Récupère les valeurs affichées dans Google Sheets sans conversion
    automatique des nombres par gspread.
    """

    data = sheet.get_all_values(
        value_render_option="FORMATTED_VALUE"
    )

    if not data:
        return pd.DataFrame()

    # Première ligne : noms des colonnes
    headers = data[0]

    # Ignore les lignes complètement vides et complète les cellules
    # manquantes pour conserver l'alignement avec les en-têtes.
    lignes = []

    for row in data[1:]:
        if not any(str(value).strip() for value in row):
            continue

        row = row + [""] * (len(headers) - len(row))
        lignes.append(dict(zip(headers, row[:len(headers)])))

    return pd.DataFrame(lignes, columns=headers)


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

    movies = charger_feuille_en_dataframe(sheet)

    if movies.empty:
        return movies

    # --------------------------
    # Conversion des dates
    # --------------------------

    if "watched_at" in movies.columns:
        movies["watched_at"] = pd.to_datetime(
            movies["watched_at"].astype("string").str.strip().str.lstrip("'"),
            format="%Y-%m-%d",
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

    series = charger_feuille_en_dataframe(sheet)

    if series.empty:
        return series

    # --------------------------
    # Conversion des dates
    # --------------------------

    for col in ["first_seen", "last_watch"]:
        if col in series.columns:
            series[col] = pd.to_datetime(
                series[col],
                errors="coerce",
                dayfirst=True
            )

    # --------------------------
    # Conversion des nombres
    # --------------------------

    for col in ["episodes", "progress", "score"]:
        if col in series.columns:
            series[col] = convertir_nombre(series[col])

    return series
