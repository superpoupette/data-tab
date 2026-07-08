import xml.etree.ElementTree as ET
import pandas as pd


def load_myanimelist(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()

    animes = []

    for anime in root.findall("anime"):
        animes.append({
            "title": anime.findtext("series_title"),
            "type": "anime",
            "status": anime.findtext("my_status"),
            "episodes": int(anime.findtext("series_episodes") or 0),
            "progress": int(anime.findtext("my_watched_episodes") or 0),
            "score": int(anime.findtext("my_score") or 0),
            "start_date": anime.findtext("my_start_date"),
            "finish_date": anime.findtext("my_finish_date"),
        })

    animes = pd.DataFrame(animes)

    animes["start_date"] = pd.to_datetime(
        animes["start_date"],
        errors="coerce"
    )

    animes["finish_date"] = pd.to_datetime(
        animes["finish_date"],
        errors="coerce"
    )

    return animes


def tab_myanimelist():
    return load_myanimelist("data/animelist.xml")