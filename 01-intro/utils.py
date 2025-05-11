# download the necessary data
# this looks like green taxi data from NYC site, for January 2021
# https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
import os 
import urllib 
import pandas as pd

DATA_DIR="./data"
READ_BUFFER=1024

def load_file(file):
    return pd.read_parquet(f"{DATA_DIR}/{file}")

def load_data(file):
    df = load_file(file)
    return clean_and_calculate_fields(df)


def clean_and_calculate_fields(df):

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)

    #df = df[(df.duration >= 1) & (df.duration <= 24*60)]

    categorical = ['PULocationID', 'DOLocationID']

    df[categorical] = df[categorical].astype(str)
    return df 

def download_data_files(use_cache=True,*args):
    os.makedirs(DATA_DIR, exist_ok=True) 
    for file in args:
        print(f"Downloading {file}")
        download_data(file, use_cache=use_cache) 
        df = pd.read_parquet(f"{DATA_DIR}/{file}")
        print(f"Downloaded {file} with {df.shape[0]} rows and {df.shape[1]} columns")

def download_data(file, use_cache=True):
    LOCAL_STORAGE=f"{DATA_DIR}/{file}"
    if use_cache and os.path.isfile(LOCAL_STORAGE):
        return # don't do anything. we already downloaded this.
    local_filename, _ =  urllib.request.urlretrieve(f"https://d37ci6vzurychx.cloudfront.net/trip-data/{file}")
    with open(local_filename, "rb") as f:
        with open(LOCAL_STORAGE, "wb") as d: 
            while rBytes := f.read(READ_BUFFER):
                d.write(rBytes)
