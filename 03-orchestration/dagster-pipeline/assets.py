import dagster as dg 
from pathlib import Path 
import pickle
import mlflow
import pandas as pd
import urllib
import urllib.request
import os
import sys
import logging
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error

logging.basicConfig(
    level=logging.INFO, 
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s: %(message)s ",
    datefmt="%Y-%m-%d %H:%M:%S %z",
)
logger= logging.getLogger(__name__)

EXPERIMENT_NAME='HW_03_YELLOW_TAXI_DURATION_PREDICTION'
mlflow.set_tracking_uri("http://127.0.0.1:5000")# we'll want to move this to a resource in dagster
mlflow.set_experiment(EXPERIMENT_NAME)
mlflow.sklearn.autolog()


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

def training_data():
    df = pd.read_parquet(PREPROCESSED_DATA)
    dv = DictVectorizer()
    dicts = df[['PULocationID','DOLocationID','trip_distance']].to_dict(orient='records')
    X_train = dv.fit_transform(dicts)
    Y_train = df['duration']

    return dv, X_train, Y_train 

def dump(obj, path):
    with open(path, "wb") as f_out:
        pickle.dump(obj, f_out)

PREPROCESSOR_PATH=f"{DATA_DIR}/models/preprocessor.pkl"

@dg.asset(deps=[preprocessed_data])
def trained_model():
    dv, X_train, Y_train = training_data()

    with mlflow.start_run():
        logger.info(f"Training model")
        lr = LinearRegression()
        lr.fit(X_train,Y_train) 
        params = lr.get_params()
        logger.info("Model trained")
        mlflow.log_params(params)
        dump(dv,PREPROCESSOR_PATH)

        mlflow.log_artifact(PREPROCESSOR_PATH, "preprocessor.pkl")
        mlflow.sklearn.log_model(
            sk_model=lr,
            artifact_path='sklearn-duration-prediction',
            registered_model_name='sklearn-linear-reg-model',
        )
        logger.info("Model registered")
        logger.info(f"Model intercept {lr.intercept_}")
    return dg.Output(
        value=lr,
        metadata={
            "model_type": "sklearn.linear_model.LinearRegression",
            "params": lr.get_params(),
        },
    )

    
    

defs = dg.Definitions(assets=[raw_data, preprocessed_data, trained_model])

