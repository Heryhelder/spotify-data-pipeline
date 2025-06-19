import pandas as pd
import os
import datetime

def csv_to_parquet(csv_file):
    if csv_file is None:
        return

    ROOT_DATA_PATH = "Data/parquet"

    if not os.path.exists(ROOT_DATA_PATH):
        os.makedirs(ROOT_DATA_PATH)

    DEST_DATA_PATH = os.path.join(ROOT_DATA_PATH, f"spotify_data_{datetime.datetime.now().strftime("%Y-%m-%d")}.parquet")

    df = pd.read_csv(csv_file)
    df.to_parquet(DEST_DATA_PATH)