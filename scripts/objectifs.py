import pandas as pd

from scripts.importation_2026 import prepare_2026


def sport_2026():
    data = prepare_2026()

    activites = [
        "Danse",
        "Muscu",
        "Stretch",
        "Course",
        "Escalade",
        "Randonnée",
        "Autre",
    ]

    total = (
        data[activites]
        .apply(pd.to_numeric, errors="coerce")
        .fillna(0)
        .sum()
        .sum()
    )

    return total


def pompes_2026():
    data = prepare_2026()

    pompes = (
        pd.to_numeric(
            data["Pompes"],
            errors="coerce"
        )
        .fillna(0)
        .sum()
    )

    return int(pompes)