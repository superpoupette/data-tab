from scripts.google_drive import load_csv_from_drive
from scripts.google_drive import load_excel_from_drive
from scripts.importation_2026 import clean_2026

from scripts.importation_2024 import clean_csv as clean_2024
from scripts.importation_2025 import clean_csv as clean_2025


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


def load_year(year):

    if year not in FILES_DRIVE:
        raise ValueError(
            f"Aucune donnée disponible pour {year}"
        )


    config = FILES_DRIVE[year]


    data = load_csv_from_drive(
        config["id"],
        separator=config["separator"]
    )


    if year == 2024:
        data = clean_2024(data)


    if year == 2025:
        data = clean_2025(data)


    return data


def load_2026():

    data = load_excel_from_drive(
        FILES_DRIVE[2026],
        sheet_name="DATA"
    )

    data = clean_2026(data)

    return data


from scripts.google_drive import load_csv_from_drive
from scripts.importation_hevy import prepare_data


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