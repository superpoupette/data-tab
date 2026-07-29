import pandas as pd


def clean_csv(data2024):

    # Conversion des dates
    data2024["Date"] = pd.to_datetime(
        data2024["Date"],
        dayfirst=True,
        format="mixed"
    )


    # Renommage des colonnes chorées
    rename_columns = {

        "Chorée": "Choree1_morceau",
        "Chorée_1": "Choree2_morceau",
        "Chorée_3": "Choree3_morceau",
        "Chorée_8": "Choree4_morceau",
        "Chorée_10": "Choree5_morceau",

        "Temps": "Choree1_duree",
        "Temps_2": "Choree2_duree",
        "Temps_4": "Choree3_duree",
        "Temps_9": "Choree4_duree",
        "Temps_11": "Choree5_duree",
    }


    # Renomme uniquement les colonnes présentes
    data2024 = data2024.rename(
        columns={
            old: new
            for old, new in rename_columns.items()
            if old in data2024.columns
        }
    )


    return data2024