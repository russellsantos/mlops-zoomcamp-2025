import os
import pickle
import click
import mlflow

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error
mlflow.set_tracking_uri('sqlite:///data/mlflow.db')
mlflow.set_experiment('initial-nyc-taxi-experiment')
mlflow.autolog()
def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
def run_train(data_path: str):
    train_path = os.path.join(data_path, "train.pkl")
    val_path = os.path.join(data_path, "val.pkl")
    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

    with mlflow.start_run():
        max_depth = 10
        random_state = 0
        mlflow.set_tag("developer","russell")
        mlflow.set_tag("project", "nyc-taxi")
        mlflow.log_param("train-data-path", train_path )
        mlflow.log_param("val-data-path", val_path )
        rf = RandomForestRegressor(max_depth=max_depth, random_state=random_state)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)

        rmse = root_mean_squared_error(y_val, y_pred)
        print("RMSE ", rmse)


if __name__ == '__main__':
    run_train()
