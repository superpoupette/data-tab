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