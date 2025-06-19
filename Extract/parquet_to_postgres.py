import pandas as pd
import psycopg2

def get_parquet_data(parquet_file):
    if parquet_file is None:
        return

    df = pd.read_parquet(parquet_file)

    return df

def connect_to_postgres():
    dbname = "postgres"
    user = "postgres"
    password = "mysecretpassword"
    host = "localhost"

    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)

    return conn

def insert_data_postgres():
    conn = connect_to_postgres()
    cursor = conn.cursor()

    data = get_parquet_data("Data/parquet/spotify_data_2025-06-18.parquet")

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

insert_data_postgres()