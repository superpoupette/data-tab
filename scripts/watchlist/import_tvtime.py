import pandas as pd


def load_tvtime_movies(filepath):

    return pd.read_csv(filepath)


def load_tvtime_series(filepath):

    return pd.read_csv(filepath)


def load_tvtime_series_episodes(filepath):

    return pd.read_csv(filepath)



import xml.etree.ElementTree as ET


def load_myanimelist(filepath):

    tree = ET.parse(filepath)

    root = tree.getroot()

    animes = []

    for anime in root.findall("anime"):

        animes.append(
            {
                "tvdb_id": anime.findtext("series_animedb_id"),
                "title": anime.findtext("series_title"),
                "episodes": int(
                    anime.findtext("series_episodes") or 0
                ),
                "progress": int(
                    anime.findtext("my_watched_episodes") or 0
                ),
                "rating": int(
                    anime.findtext("my_score") or 0
                ),
                "status": anime.findtext("my_status"),
            }
        )

    return pd.DataFrame(animes)