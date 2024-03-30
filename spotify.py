import spotipy
from spotipy.oauth2 import SpotifyOAuth
import urllib.parse
import os
import dotenv

dotenv.load_dotenv()

auth = SpotifyOAuth(
    client_id=os.environ["SPOTIFY_CLIENT_ID"],
    client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
    redirect_uri="https://spotipi-auth.vercel.app/",
    scope="user-library-read",
    open_browser=False,
)


def get_auth_domain(redirect: str):
    auth_domain = f"https://spotipi-auth.vercel.app/?spotify={urllib.parse.quote(auth.get_authorize_url())}&redirect={urllib.parse.quote(redirect)}"
    return auth_domain


def get_access_token(code: str):
    auth.get_access_token(code)


def print_top():
    sp = spotipy.Spotify(auth_manager=auth)

    results = sp.current_user_saved_tracks()
    for idx, item in enumerate(results["items"]):
        track = item["track"]
        print(idx, track["artists"][0]["name"], " - ", track["name"])
