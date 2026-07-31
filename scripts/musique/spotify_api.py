import re
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



def extraire_spotify_id(url):

    match = re.search(
        r"album/([a-zA-Z0-9]+)",
        url
    )

    if match:
        return match.group(1)

    return None



def enrichir_album_depuis_url(url):

    spotify_id = extraire_spotify_id(url)

    if not spotify_id:
        return None


    sp = get_spotify_client()


    details = sp.album(
        spotify_id
    )


    artiste = details["artists"][0]


    return {

        "spotify_id":
            details["id"],

        "spotify_url":
            details["external_urls"]["spotify"],

        "cover_url":
            details["images"][0]["url"]
            if details["images"]
            else "",

        "spotify_date_sortie":
            details["release_date"],

        "nb_titres":
            details["total_tracks"],

        "spotify_artiste":
            artiste["name"],

        "spotify_album":
            details["name"]

    }