import pandas as pd
import os
from datetime import datetime
import boto3

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def create_data():
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    return pd.DataFrame(data, columns=columns)

S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL', 'http://localhost:4566')
INPUT_FILE_PATTERN= os.getenv('INPUT_FILE_PATTERN', 's3://nyc-duration/input/year={year:04d}/month={month:02d}/input.parquet')
OUTPUT_FILE_PATTERN = os.getenv('OUTPUT_FILE_PATTERN', 's3://nyc-duration/output/year={year:04d}/month={month:02d}/predictions.parquet')

def create_bucket_if_not_exists(bucket_name):
    s3 = boto3.client(
        's3', 
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id='test',
        aws_secret_access_key='test',
        region_name='us-east-1'
    )
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} already exists")
    except Exception as e:
        print(f"Bucket {bucket_name} does not exist. Creating it.")
        # For us-east-1 (default region), don't specify LocationConstraint
        s3.create_bucket(Bucket=bucket_name)

def create_and_save_test_data(): 
    create_bucket_if_not_exists('nyc-duration')
    
    df_input = create_data()
    options = {
        'client_kwargs': {
            'endpoint_url': S3_ENDPOINT_URL,
        },
    }
    input_file = INPUT_FILE_PATTERN.format(year=2023, month=1)
    print(f"Writing test data to {input_file}")
    print(f"Storage options: {options}")
    df_input.to_parquet(
        path=input_file,
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=options,
    )

def run_batch_command():
    
    cmd = 'python batch.py 2023 1'
    print(f"Running command: {cmd}")
    os.system(cmd, )

def check_output():
    print("Checking output...")  # Placeholder for actual output checking logic
    output_file = OUTPUT_FILE_PATTERN.format(year=2023, month=1)
    print(f"Output file should be at: {output_file}")
    options = {
        'client_kwargs': {
            'endpoint_url': S3_ENDPOINT_URL,
        },
    }
    df = pd.read_parquet(path=output_file, storage_options=options)
    assert df.shape[0] == 2, "Output DataFrame should have 2 rows"
    pred_mean = round(df['predicted_duration'].mean(),1)
    pred_sum = round(df['predicted_duration'].sum(),1)
    assert pred_mean == 18.1, f"Expected mean duration to be 18.1, but got {pred_mean}"
    assert pred_sum == 36.3, f"Expected sum duration to be 36.1, but got {pred_sum}"

if __name__ == "__main__":
    create_and_save_test_data()
    run_batch_command()
    check_output()


