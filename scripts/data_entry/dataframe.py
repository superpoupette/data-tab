import pandas as pd


def create_today_dataframe():
    return pd.DataFrame(columns=[
        "date",
        "best_moment"
    ])


def add_today_entry(df, today_date, best_moment):
    new_row = pd.DataFrame([{
        "date": today_date,
        "best_moment": best_moment
    }])

    df = pd.concat([df, new_row], ignore_index=True)

    return df