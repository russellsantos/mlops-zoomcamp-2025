#!/usr/bin/env python
# coding: utf-8
from argparse import ArgumentParser
import pickle
import pandas as pd




with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)



categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df




def run(year, month):
    df = read_data('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet')
    dicts= df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)

    print(f"Mean predicted duration: {y_pred.mean()}")
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    df.head()
    output_file='output.parquet'
    df_result = df[['ride_id']].copy()
    df_result['predicted_duration']=y_pred
    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )

def create_parser():
    parser = ArgumentParser()
    parser.add_argument("year",  type=int, help="Year of the data (e.g., 2023)")
    parser.add_argument("month", type=int, help="Month of the data (e.g., 3 for March)")
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    run(args.year, args.month)

if __name__=="__main__":
    main()
