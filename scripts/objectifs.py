import pandas as pd

from scripts.importation_2026 import prepare_2026


def pompes_2026():

    data = prepare_2026()

    if "Pompes" not in data.columns:
        return 0

    # Conversion en numérique
    pompes = pd.to_numeric(
        data["Pompes"],
        errors="coerce"
    )

    # Suppression de la première ligne de la colonne
    pompes = pompes.iloc[1:]

    # Somme
    total = pompes.fillna(0).sum()

    return int(total)