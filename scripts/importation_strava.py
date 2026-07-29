import pandas as pd
from scripts.google_drive import load_csv_from_drive
from scripts.data_loader import STRAVA_FILE


def charger_donnees_strava():

    df = load_csv_from_drive(
        STRAVA_FILE["id"],
        separator=STRAVA_FILE["separator"]
    )

    # Conversion des dates Strava en français
    mois_fr = {
        "janv.": "Jan",
        "févr.": "Feb",
        "mars": "Mar",
        "avr.": "Apr",
        "mai": "May",
        "juin": "Jun",
        "juil.": "Jul",
        "août": "Aug",
        "sept.": "Sep",
        "oct.": "Oct",
        "nov.": "Nov",
        "déc.": "Dec"
    }

    for fr, en in mois_fr.items():
        df["Date de l'activité"] = (
            df["Date de l'activité"]
            .astype(str)
            .str.replace(fr, en, regex=False)
        )

    df["Date de l'activité"] = pd.to_datetime(
        df["Date de l'activité"],
        format="%d %b %Y, %H:%M:%S",
        errors="coerce"
    )
    
    #correction distance
    df["Distance"] = (
        df["Distance"]
        .astype(str)
        .str.replace('"', '', regex=False)
        .str.replace(",", ".", regex=False)
    )

    df["Distance"] = pd.to_numeric(df["Distance"], errors="coerce")

    df["Vitesse moyenne"] = pd.to_numeric(df["Vitesse moyenne"], errors="coerce")
    df["Durée de déplacement"] = pd.to_numeric(df["Durée de déplacement"], errors="coerce")

    return df