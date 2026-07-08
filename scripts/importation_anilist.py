import requests
import pandas as pd


def load_anilist(username):

    query = """
    query ($userName: String) {
      MediaListCollection(userName: $userName, type: ANIME) {
        lists {
          entries {
            media {
              title {
                romaji
                english
              }
              type
              episodes
              duration
              seasonYear
            }
            status
            score
            progress
            startedAt {
              year
              month
              day
            }
            completedAt {
              year
              month
              day
            }
          }
        }
      }
    }
    """

    variables = {
        "userName": username
    }

    response = requests.post(
        "https://graphql.anilist.co",
        json={
            "query": query,
            "variables": variables
        }
    )

    data = response.json()

    entries = []

    for list_ in data["data"]["MediaListCollection"]["lists"]:
        for entry in list_["entries"]:
            media = entry["media"]

            entries.append({
                "title": media["title"]["romaji"],
                "year": media["seasonYear"],
                "status": entry["status"],
                "episodes": media["episodes"],
                "duration": media["duration"],
                "progress": entry["progress"],
                "watched_at": entry["completedAt"]
            })

    return pd.DataFrame(entries)