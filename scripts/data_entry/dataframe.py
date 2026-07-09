import pandas as pd
import os


CSV_FILE = "today_data.csv"


def create_today_dataframe():

    columns = [
        "date",
        "best_moment",
        "people_seen",
        "people_work",
        "sommeil",
        "Choree1_morceau",
        "Choree1_duree"
    ]

    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)

    else:
        df = pd.DataFrame(columns=columns)
        df.to_csv(
            CSV_FILE,
            index=False,
            encoding="utf-8-sig"
        )

    return df


def add_today_entry(
    df,
    today_date,
    best_moment,
    people_seen,
    people_work,
    sommeil,
    Choree1_morceau,
    Choree1_duree
):

    new_row = pd.DataFrame([{
        "date": today_date,
        "best_moment": best_moment,
        "people_seen": people_seen,
        "people_work": people_work,
        "sommeil": sommeil,
        "Choree1_morceau": Choree1_morceau,
        "Choree1_duree": Choree1_duree
    }])

    df = pd.concat(
        [df, new_row],
        ignore_index=True
    )

    return df


def save_dataframe_csv(df):

    df.to_csv(
        CSV_FILE,
        index=False,
        encoding="utf-8-sig"
    )