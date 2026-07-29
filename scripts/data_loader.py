from scripts.google_drive import load_csv_from_drive

from scripts.importation_2024 import clean_csv as clean_2024
from scripts.importation_2025 import clean_csv as clean_2025


FILES_DRIVE = {

    2024: "17onD34HL2QKC4OP0oPrvt_ynfq63XO0Z",

    2025: "1dBvQMHY3gLOIEmTWvx21MY-PKeawLmms"

}



def load_year(year):

    if year not in FILES_DRIVE:
        raise ValueError(
            f"Aucune donnée disponible pour {year}"
        )


    data = load_csv_from_drive(
        FILES_DRIVE[year]
    )


    if year == 2024:
        data = clean_2024(data)


    if year == 2025:
        data = clean_2025(data)


    return data