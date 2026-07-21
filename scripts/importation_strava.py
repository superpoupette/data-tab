import pandas as pd




df = pd.read_csv(
        "data/strava_activities.csv",
        encoding="utf-8",
        low_memory=False
    )

    return df