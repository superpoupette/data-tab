from scripts.musique.spotify_api import get_spotify_client


sp = get_spotify_client()

result = sp.search(
    q="album:Random Access Memories artist:Daft Punk",
    type="album",
    limit=1
)

print(
    result["albums"]["items"][0]["name"]
)