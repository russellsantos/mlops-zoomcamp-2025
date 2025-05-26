import os
import pandas as pd
import urllib.request 
import click
import urllib
from pathlib import Path

READ_BUFFER=1024

EXPERIMENT_TRACKING_FOLDER:Path =Path(__file__).parent.parent
DATA_DIR:Path =EXPERIMENT_TRACKING_FOLDER.joinpath('data')

def download_data_files(data_dir, files):
    print(f"Downloading {files} to {data_dir}")
    os.makedirs(data_dir, exist_ok=True) 
    for file in files:
        download_data(file, data_dir=data_dir, use_cache=True) 
        df = pd.read_parquet(f"{data_dir}/{file}")
        print(f"Downloaded {file} with {df.shape[0]} rows and {df.shape[1]} columns")

def download_data(file, data_dir=DATA_DIR, use_cache=True):
    print(f"Downloading {file} ... ")
    LOCAL_STORAGE=f"{data_dir}/{file}"
    if use_cache and os.path.isfile(LOCAL_STORAGE):
        return # don't do anything. we already downloaded this.
    local_filename, _ =  urllib.request.urlretrieve(f"https://d37ci6vzurychx.cloudfront.net/trip-data/{file}")
    with open(local_filename, "rb") as f:
        with open(LOCAL_STORAGE, "wb") as d: 
            while rBytes := f.read(READ_BUFFER):
                d.write(rBytes)


@click.command 
@click.option(
    "--raw_data_path",
    type=Path,
    default=DATA_DIR.absolute(),
    show_default=True,
    help="Location where the raw NYC taxi trip data will be saved",
)
@click.option(
    "--files",
    type=str,
    default=['green_tripdata_2023-01.parquet','green_tripdata_2023-02.parquet','green_tripdata_2023-03.parquet'],
    multiple=True,
    show_default=True, 
    help="List of files to download",
)
def main(raw_data_path, files): 
    download_data_files(raw_data_path, files)


if __name__ == "__main__":
    main()