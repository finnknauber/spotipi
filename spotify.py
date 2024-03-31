import spotipy
from spotipy.oauth2 import SpotifyOAuth
import urllib.parse
import os
from dotenv import load_dotenv
import socket

load_dotenv()

auth = SpotifyOAuth(
    client_id=os.environ["SPOTIFY_CLIENT_ID"],
    client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
    redirect_uri="https://spotipi-auth.vercel.app/",
    scope="user-library-read streaming user-read-playback-state user-modify-playback-state",
    open_browser=False,
)


def get_auth_domain(redirect: str):
    auth_domain = f"https://spotipi-auth.vercel.app/?spotify={urllib.parse.quote(auth.get_authorize_url())}&redirect={urllib.parse.quote(redirect)}"
    return auth_domain


def get_access_token(code: str):
    auth.get_access_token(code)


def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return f"Error: {e}"


def print_top():
    sp = spotipy.Spotify(auth_manager=auth)

    results = sp.current_user_saved_tracks()
    for idx, item in enumerate(results["items"]):
        track = item["track"]
        print(idx, track["artists"][0]["name"], " - ", track["name"])


def play_test(link):
    sp = spotipy.Spotify(auth_manager=auth)
    for device in sp.devices()["devices"]:
        if device["is_active"]:
            try:
                sp.start_playback(
                    device_id=device["id"],
                    uris=["spotify:"+link],
                )
            except:
                print("Error playing")
