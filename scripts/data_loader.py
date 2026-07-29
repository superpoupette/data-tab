from scripts.google_drive import load_csv_from_drive
from scripts.importation_2024 import clean_csv


FILES_DRIVE = {

    2024: "17onD34HL2QKC4OP0oPrvt_ynfq63XO0Z"

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
        data = clean_csv(data)


    return data