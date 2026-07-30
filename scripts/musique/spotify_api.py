import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st


def get_spotify_client():

    auth_manager = SpotifyClientCredentials(
        client_id=st.secrets["spotify"]["client_id"],
        client_secret=st.secrets["spotify"]["client_secret"]
    )

    return spotipy.Spotify(
        auth_manager=auth_manager
    )



def rechercher_album(album, artiste):

    sp = get_spotify_client()

    result = sp.search(
        q=f"album:{album} artist:{artiste}",
        type="album",
        limit=5
    )

    albums = result["albums"]["items"]

    if not albums:
        return None

    # On prend le premier résultat pour l'instant
    return albums[0]



def enrichir_album(album, artiste):

    sp = get_spotify_client()

    resultat = rechercher_album(
        album,
        artiste
    )

    if resultat is None:
        return None


    details = sp.album(
        resultat["id"]
    )


    return {

        "spotify_id": details["id"],

        "spotify_url": details["external_urls"]["spotify"],

        "cover_url": details["images"][0]["url"]
        if details.get("images")
        else "",

        "spotify_date_sortie": details["release_date"],

        "nb_titres": details["total_tracks"],

        "popularite": resultat.get("popularity", ""),

        "spotify_artiste":
            resultat["artists"][0]["name"]
    }