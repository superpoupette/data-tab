import pandas as pd

from scripts.importation_2026 import prepare_2026
from scripts.importation_hevy import load_workouts, clean_dates


def pompes_2026():

    # ==========================
    # Pompes depuis Excel 2026
    # ==========================

    data = prepare_2026()

    total_excel = 0

    if "Pompes" in data.columns:

        pompes_excel = pd.to_numeric(
            data["Pompes"],
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

    workouts = load_workouts(
        "data/workouts.csv"
    )

    workouts = clean_dates(
        workouts
    )


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