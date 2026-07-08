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
        })

    return pd.DataFrame(animes)

def clean_animes(animes):
    animes["status"] = animes["status"].replace(
        {
            "Completed": "watched",
            "Watching": "continuing",
            "Plan to Watch": "to_watch",
            "On-Hold": "paused",
            "Dropped": "stopped"
        }
    )

    return animes

def tab_myanimelist():
    animes = load_myanimelist("data/animelist.xml")
    animes = clean_animes(animes)
    return animes