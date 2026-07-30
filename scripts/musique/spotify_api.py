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


def enrichir_album(spotify_id):

    sp = get_spotify_client()

    try:

        details = sp.album(
            spotify_id
        )

        artiste = details["artists"][0]

        # récupération des genres artiste
        artiste_details = sp.artist(
            artiste["id"]
        )

        genres = ", ".join(
            artiste_details.get("genres", [])
        )


        return {

            "spotify_id": details["id"],

            "spotify_url": details["external_urls"]["spotify"],

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
                details["name"],

            "spotify_genres":
                genres
        }


    except Exception as e:

        print(
            f"Erreur Spotify {spotify_id} : {e}"
        )

        return None