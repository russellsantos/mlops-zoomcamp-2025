import dagster as dg 
from pathlib import Path 
import pandas as pd
import urllib
import urllib.request
import os
import logging


logger= logging.getLogger(__name__)

READ_BUFFER=1024
ORCHESTRATION_FOLDER:Path =Path(__file__).parent.parent
DATA_DIR:Path =ORCHESTRATION_FOLDER.joinpath('data')
def download_data(url, local_path, use_cache=True):
    logger.info(f"Downloading {url} ... ")
    if use_cache and os.path.isfile(local_path):
        return # don't do anything. we already downloaded this.
    local_filename, _ =  urllib.request.urlretrieve(url)
    with open(local_filename, "rb") as f:
        with open(local_path, "wb") as d: 
            while rBytes := f.read(READ_BUFFER):
                d.write(rBytes)

def read_dataframe(filename):
    df = pd.read_parquet(filename)

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    
    return df
TAXI_DATA_URL='https://d37ci6vzurychx.cloudfront.net/trip-data'
RAW_DATA_SOURCE=f"{TAXI_DATA_URL}/yellow_tripdata_2023-03.parquet"
RAW_DATA_DOWNLOADED=f"{DATA_DIR}/raw/yellow_tripdata_2023-03.parquet"
@dg.asset(
        
)
def raw_data():
    download_data(RAW_DATA_SOURCE, RAW_DATA_DOWNLOADED, use_cache=True)
    df = pd.read_parquet(RAW_DATA_DOWNLOADED)
    message = f"Downloaded file with shape {df.shape}"
    logger.info(message)
    return dg.MaterializeResult(
        metadata={
            "dagster/uri": RAW_DATA_SOURCE,
            "dagster/row_count": df.shape[0],
            "column_count": df.shape[1],
        }
    )

PREPROCESSED_DATA=f'{DATA_DIR}/processed/preprocessed.parquet' 
@dg.asset(deps=[raw_data])
def preprocessed_data():
    df = read_dataframe(RAW_DATA_DOWNLOADED)
    df.to_parquet(PREPROCESSED_DATA)
    message = f"Processed data with shape {df.shape}"
    logger.info(message)
    return dg.MaterializeResult(
        metadata={
            "dagster/uri": RAW_DATA_SOURCE,
            "dagster/row_count": df.shape[0],
            "column_count": df.shape[1],
        }
    )

defs = dg.Definitions(assets=[raw_data, preprocessed_data])

