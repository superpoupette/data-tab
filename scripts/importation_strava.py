import pandas as pd
import streamlit as st


def charger_donnees_strava():

    df = pd.read_csv(
        "data/strava_activities.csv",
        encoding="utf-8",
        low_memory=False
    )

    # Conversion de la date
    df["Date de l'activité"] = pd.to_datetime(
        df["Date de l'activité"],
        format="mixed",
        dayfirst=True,
        errors="coerce"
    )

    return df