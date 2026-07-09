import pandas as pd


def derniers_visionnages(movies, series):
    watched_movies = (
        movies[movies["status"] == "watched"]
        .rename(columns={"watched_at": "date"})
        .assign(episode=pd.NA)
        [["title", "type", "status", "episode", "date", "rating"]]
    )

    watched_series = (
        series[series["status"].isin(["up_to_date", "continuing"])]
        .rename(columns={"last_watch": "date",
                         "last_episode": "episode"})
        .assign(rating=pd.NA)
        [["title", "type", "status", "episode", "date", "rating"]]
    )

    derniers_visionnages = pd.concat(
        [watched_movies, watched_series],
        ignore_index=True
    )

    derniers_visionnages = derniers_visionnages.sort_values(
        by="date",
        ascending=False
    )

    return derniers_visionnages