# Overview

Link: https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/02-experiment-tracking
These commands are commands I used thorughout this homework. I've kept them here for my own reference.

Note: commands here are run assuming you're in the `02-experiment-tracking` folder.

# Downloading the data

## Create the data folders

`$ mkdir -p data/raw`

`$ uv run ./homework/download_data.py`

Note that this uses the default download directory `./data/raw` when downloading the data.

# Preprocessing

## Create the processed folders

`$ mkdir -p data/processed`

This will be where we wil store the processed data.

## Running the pre-processing script.
This script does pre-processing on the downloaded data, and then generates processed data in the `--dest_path` argument. This will calculate relevant features, and split 
data into test, traing and validation data sets.
`$ uv run ./homework/preprocess_data.py --raw-data-dir ./data/raw --dest_path ./data/processed`

# Training  and Logging

## Running the mlflow ui

`$ uv run mlflow --backend-store-uri sqlite:///data/mlflow.db`

This will run the mlflow ui, which is accessible at http://127.0.0.1:5000

## Training the model

`$ uv run homework/train.py --data_path data/processed/`

# Launch the tracking server 

 - Make the directory first

`$ mkdir -p .data/artifacts`
`$ uv run mflow server --backend-store-uri data/mlflow.db --artifacts-destination file://data/artifacts`

# Hyperparameter Tuning

## running the tuning

`$ uv run homework/hpo.py --data_path data/processed`