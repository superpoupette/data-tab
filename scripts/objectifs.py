import pandas as pd

from scripts.importation_2026 import prepare_2026


def pompes_2026():

    data = prepare_2026()

    if "Pompes" not in data.columns:
        return 0

    pompes = (
        pd.to_numeric(
            data["Pompes"].iloc[1:],  # ignore la première ligne
            errors="coerce"
        )
        .fillna(0)
        .sum()
    )

    return int(pompes)