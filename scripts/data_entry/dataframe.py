import pandas as pd


def create_today_dataframe():
    return pd.DataFrame(columns=[
        "date",
        "best_moment",
        "people_seen",
        "people_work",
        "sommeil",
        "Choree1_morceau",
        "Choree1_duree"
    ])


def add_today_entry(df, today_date, best_moment, people_seen, people_work, sommeil, Choree1_morceau, Choree1_duree):

    new_row = pd.DataFrame([{
        "date": today_date,
        "best_moment": best_moment,
        "people_seen": people_seen,
        "people_work": people_work,
        "sommeil": sommeil,
        "Choree1_morceau": Choree1_morceau,
        "Choree1_duree": Choree1_duree
    }])

    df = pd.concat([df, new_row], ignore_index=True)

    return df