import pandas as pd

def create_today_dataframe():
    return pd.DataFrame(columns=[
        "date",
        "best_moment"
    ])