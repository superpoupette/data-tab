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


    # Informations album
    details = sp.album(
        resultat["id"]
    )


    # Informations artiste
    artiste_id = (
        resultat["artists"][0]["id"]
    )

    details_artiste = sp.artist(
        artiste_id
    )


    genres = ", ".join(
        details_artiste.get(
            "genres",
            []
        )
    )


    return {

        "spotify_id": details.get(
            "id",
            ""
        ),

        "spotify_date_sortie": details.get(
            "release_date",
            ""
        ),

        "nb_titres": details.get(
            "total_tracks",
            ""
        ),

        "cover_url": (
            details["images"][0]["url"]
            if details.get("images")
            else ""
        ),

        "spotify_artiste": (
            resultat["artists"][0]["name"]
        ),

        "spotify_album": (
            details.get(
                "name",
                ""
            )
        ),

        "spotify_genres": genres
    }