import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os
import datetime
import psycopg2

class SpotifyData:
    root_data_path = None

    def __init__(self):
        self.root_data_path = "data"

    def get_spotify_data(self, date_unix_timestamp):
        scope = "user-read-recently-played"

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        results = sp.current_user_recently_played(after=date_unix_timestamp)

        return results

    def save_spotify_data(self, data):
        if data is None:
            return

        if not os.path.exists(os.path.join(self.root_data_path, "csv")):
            os.makedirs(os.path.join(self.root_data_path, "csv"))

        dest_data_path = os.path.join(self.root_data_path, "csv", f"spotify_data_{datetime.datetime.now().strftime("%Y-%m-%d")}.csv")

        df = pd.json_normalize(data["items"])
        df.to_csv(dest_data_path, index=False)

        return dest_data_path
    
    def csv_to_parquet(self, csv_file_path):
        if csv_file_path is None:
            return

        if not os.path.exists(os.path.join(self.root_data_path, "parquet")):
            os.makedirs(os.path.join(self.root_data_path, "parquet"))

        dest_data_path = os.path.join(self.root_data_path, "parquet", f"spotify_data_{datetime.datetime.now().strftime("%Y-%m-%d")}.parquet")

        df = pd.read_csv(csv_file_path)
        df.to_parquet(dest_data_path)

        return dest_data_path
    
    def get_parquet_data(self, parquet_file):
        if parquet_file is None:
            return

        df = pd.read_parquet(parquet_file)

        return df

    def connect_to_postgres(self):
        dbname = "postgres"
        user = "postgres"
        password = "mysecretpassword"
        host = "localhost"

        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)

        return conn

    def insert_data_postgres(self, parquet_file):
        conn = self.connect_to_postgres()
        cursor = conn.cursor()

        data = self.get_parquet_data(parquet_file)

        insert_album_data = """
            INSERT INTO "user-read-recently-played".album (id, name, release_date, total_tracks)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """

        insert_track_data = """
            INSERT INTO "user-read-recently-played".track (id, album_id, duration_ms, explicit, name, track_number, played_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """

        try:
            album_df = data[['track.album.id', 'track.album.name', 'track.album.release_date', 'track.album.total_tracks']]

            track_df = data[['track.id', 'track.album.id', 'track.duration_ms', 'track.explicit', 'track.name', 'track.track_number', 'played_at']]

            for row in album_df.itertuples(index=False, name=None):
                cursor.execute(insert_album_data, row)

            for row in track_df.itertuples(index=False, name=None):
                cursor.execute(insert_track_data, row)
            
            conn.commit()
        except Exception as e:
            print(f"Error inserting data: {e}")
        finally:
            cursor.close()
            conn.close()

