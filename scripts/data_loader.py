from scripts.google_drive import load_csv_from_drive

from scripts.importation_2024 import clean_csv as clean_2024
from scripts.importation_2025 import clean_csv as clean_2025


FILES_DRIVE = {

    2024: {
        "id": "17onD34HL2QKC4OP0oPrvt_ynfq63XO0Z",
        "separator": ";"
    },

    2025: {
        "id": "1dBvQMHY3gLOIEmTWvx21MY-PKeawLmms",
        "separator": ","
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