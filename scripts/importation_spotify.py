from pathlib import Path
import json
import pandas as pd


def charger_historique_spotify():

    dossier = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "Spotify Extended Streaming History"
    )

    fichiers = sorted(dossier.glob("Streaming_History_Audio*.json"))

    data = []

    for fichier in fichiers:
        with open(fichier, "r", encoding="utf-8") as f:
            data.extend(json.load(f))

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
    df = df[df["master_metadata_track_name"].notna()]

    return df