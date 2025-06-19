import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os
import datetime

def get_spotify_data():
    scope = "user-read-recently-played"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    results = sp.current_user_recently_played()

    return results

def save_spotify_data(data):
    if data is None:
        return
    
    ROOT_DATA_PATH = "Data/csv"

    if not os.path.exists(ROOT_DATA_PATH):
        os.makedirs(ROOT_DATA_PATH)

    DEST_DATA_PATH = os.path.join(ROOT_DATA_PATH, f"spotify_data_{datetime.datetime.now().strftime("%Y-%m-%d")}.csv")

    df = pd.json_normalize(data["items"])
    df.to_csv(DEST_DATA_PATH, index=False)

def main():
    data = get_spotify_data()
    save_spotify_data(data)

main()