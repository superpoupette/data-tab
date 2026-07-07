import pandas as pd


def load_csv(filepath):
    data2024 = pd.read_csv(filepath)
    return data2024


def clean_csv(data2024):

    data2024["Date"] = pd.to_datetime(
        data2024["Date"],
        format="%d/%m/%y"
    )

    data2024 = data2024.rename(
    columns={
        "Chorée": "Choree1_morceau",
        "Chorée.1": "Choree2_morceau",
        "Chorée.2": "Choree3_morceau",
        "Chorée.3": "Choree4_morceau",
        "Chorée.4": "Choree5_morceau",

        "Temps": "Choree1_duree",
        "Temps.1": "Choree2_duree",
        "Temps.2": "Choree3_duree",
        "Temps.5": "Choree4_duree",
        "Temps.6": "Choree5_duree",
        }
    )

    return data2024


def prepare_2024(filepath):
    data2024 = load_csv(filepath)
    data2024 = clean_csv(data2024)
    return data2024