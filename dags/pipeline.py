import os
import sys
from airflow.sdk import dag, task
import pendulum
from datetime import datetime

# adding src folder to path
sys.path.insert(0, './src')

from spotify_data import SpotifyData

@dag(
    schedule=None,
    start_date=pendulum.datetime(2025, 7, 1, tz="UTC"),
    catchup=False,
    tags=["spotify"],
)
def pipeline():
    spotify_data = SpotifyData()

    @task()
    def get_data():
        today_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        date_unix_timestamp = int(today_date)
        return spotify_data.get_spotify_data(date_unix_timestamp)

    @task()
    def save_data(data):
        return spotify_data.save_spotify_data(data)

    @task()
    def convert_to_parquet(dest_data_path):
        return spotify_data.csv_to_parquet(dest_data_path)

    @task()
    def insert_data_postgres(parquet_file):
        spotify_data.insert_data_postgres(parquet_file)

    @task.bash
    def dbt_transform():
        # get current directory
        current_directory = os.getcwd()
        return f"cd {current_directory}/dbt && dbt run"

    data = get_data()
    dest_data_path = save_data(data)
    parquet_file = convert_to_parquet(dest_data_path)
    insert_data_postgres(parquet_file) >> dbt_transform()

pipeline()