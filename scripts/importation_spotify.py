from pathlib import Path
import json
import pandas as pd

import pandas as pd

from scripts.data_loader import (
    load_spotify
)

def charger_historique_spotify():

    data = load_spotify()

    df = pd.DataFrame(data)

    # Conversion des dates
    df["ts"] = pd.to_datetime(df["ts"])

    # Durée en minutes
    df["minutes"] = df["ms_played"] / 60000

    # Date
    df["date"] = df["ts"].dt.date
    df["année"] = df["ts"].dt.year
    df["mois"] = df["ts"].dt.to_period("M").astype(str)
    df["jour"] = df["ts"].dt.day_name()

    # On ne garde que la musique
    df = df[
        df["master_metadata_track_name"].notna()
    ]

    return df