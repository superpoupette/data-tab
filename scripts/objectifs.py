import pandas as pd
import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

from scripts.data_loader import (
    load_year,
    load_hevy
)


def pompes_2026():

    # ==========================
    # Pompes depuis Excel 2026
    # ==========================

    data2026 = load_year(2026)

    total_excel = 0

    if "Pompes" in data2026.columns:

        pompes_excel = pd.to_numeric(
            data2026["Pompes"],
            errors="coerce"
        )

        # Suppression des lignes parasites
        pompes_excel = pompes_excel.iloc[2:]

        total_excel = (
            pompes_excel
            .fillna(0)
            .sum()
        )


    # ==========================
    # Pompes depuis Hevy
    # ==========================

    workouts, sessions = load_hevy()


    pompes_hevy = (
        workouts[
            workouts["exercise_title"] == "Push Up"
        ]["reps"]
        .fillna(0)
        .sum()
    )


    # ==========================
    # Total
    # ==========================

    total = total_excel + pompes_hevy

    return int(total)


# ==========================
# Google Sheets
# ==========================

def _sheet_objectifs():

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ]
    )

    client = gspread.authorize(credentials)

    return client.open_by_key(
        "1AZ-DudhWGHJP6-A5mXDsPgoYIgUvZL5YsVbTaK5eeMk"
    ).worksheet("objectifs")


def pages_dessin():

    sheet = _sheet_objectifs()

    valeur = sheet.acell("B2").value

    if not valeur:
        return 0

    return int(valeur)

def ajouter_page_dessin():

    sheet = _sheet_objectifs()

    actuel = pages_dessin()

    sheet.update("B2", [[actuel + 1]])

def retirer_page_dessin():

    sheet = _sheet_objectifs()

    actuel = pages_dessin()

    nouveau = max(0, actuel - 1)

    sheet.update("B2", [[nouveau]])



# ==========================
# Detox
# ==========================

def detox():

    sheet = _sheet_objectifs()

    valeur = sheet.acell("C2").value

    if not valeur:
        return 0

    return int(valeur)


def ajouter_detox():

    sheet = _sheet_objectifs()

    actuel = detox()

    nouveau = min(10, actuel + 1)

    sheet.update("C2", [[nouveau]])


def retirer_detox():

    sheet = _sheet_objectifs()

    actuel = detox()

    nouveau = max(0, actuel - 1)

    sheet.update("C2", [[nouveau]])