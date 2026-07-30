from scripts.google_drive import (
    load_csv_from_drive,
    load_excel_from_drive
)

from scripts.importation_2024 import clean_csv as clean_2024
from scripts.importation_2025 import clean_csv as clean_2025
from scripts.importation_2026 import clean_2026

from scripts.importation_hevy import prepare_data
from scripts.importation_babelio import prepare_babelio
from scripts.google_drive import (
    load_csv_from_drive,
    load_excel_from_drive,
    load_json_folder_from_drive
)


FILES_DRIVE = {

    2024: {
        "id": "17onD34HL2QKC4OP0oPrvt_ynfq63XO0Z",
        "type": "csv",
        "separator": ";"
    },

    2025: {
        "id": "1dBvQMHY3gLOIEmTWvx21MY-PKeawLmms",
        "type": "csv",
        "separator": ","
    },

    2026: {
        "id": "1PVyEQ02T-TEfofWoJAtzorob6AU8tImU",
        "type": "excel"
    }

}


OTHER_FILES = {

    "babelio": {
        "id": "1umai5aXgS22YKV3Mgk2tbvklrg9sFt_T",
        "type": "csv",
        "separator": ";",
        "encoding": "cp1252"
    }

}


HEVY_FILES = {

    "workouts": {
        "id": "16Mvq3QUPBmSQf0S2m6Y-KM6NAOgzZXLf",
        "separator": ","
    },

    "exercises": {
        "id": "1W1bPXm02LNXcd73dX5yB7odylps0Dtfa",
        "separator": ";"
    }

}


STRAVA_FILE = {
    "id": "1ns7SCQfEc4YsycnzjH2lUk7Q8gOBnNhc",
    "separator": ","
}

SPOTIFY_FOLDER = {
    "id": "1-6fwYwjbAdqN1ty4xpWf6OIm_cWWDDk6"
}


def load_year(year):

    if year not in FILES_DRIVE:
        raise ValueError(
            f"Aucune donnée disponible pour {year}"
        )


    config = FILES_DRIVE[year]


    if config["type"] == "csv":

        data = load_csv_from_drive(
            config["id"],
            separator=config["separator"]
        )


    elif config["type"] == "excel":

        data = load_excel_from_drive(
            config["id"],
            sheet_name="DATA"
        )


    else:

        raise ValueError(
            f"Type de fichier inconnu : {config['type']}"
        )



    if year == 2024:

        data = clean_2024(data)


    elif year == 2025:

        data = clean_2025(data)


    elif year == 2026:

        data = clean_2026(data)


    return data




def load_hevy():

    workouts = load_csv_from_drive(
        HEVY_FILES["workouts"]["id"],
        separator=HEVY_FILES["workouts"]["separator"]
    )


    exercices = load_csv_from_drive(
        HEVY_FILES["exercises"]["id"],
        separator=HEVY_FILES["exercises"]["separator"]
    )


    return prepare_data(
        workouts,
        exercices
    )




def load_danse_2026():

    danse = load_excel_from_drive(
        FILES_DRIVE[2026]["id"],
        sheet_name="DANSE"
    )


    return danse


def load_babelio():

    return load_csv_from_drive(
        OTHER_FILES["babelio"]["id"],
        separator=OTHER_FILES["babelio"]["separator"],
        encoding=OTHER_FILES["babelio"]["encoding"]
    )



def load_spotify():

    return load_json_folder_from_drive(
        SPOTIFY_FOLDER["id"],
        filename_prefix="Streaming_History_Audio"
    )






