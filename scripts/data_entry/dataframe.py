import pandas as pd


def create_today_dataframe():
    return pd.DataFrame(columns=[
        "date",
        "best_moment",
        "people_seen",
        "people_work"
    ])


def add_today_entry(df, today_date, best_moment, people_seen, people_work):

    new_row = pd.DataFrame([{
        "date": today_date,
        "best_moment": best_moment,
        "people_seen": people_seen,
        "people_work": people_work
    }])

    df = pd.concat([df, new_row], ignore_index=True)

    return df