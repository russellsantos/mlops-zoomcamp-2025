import datetime
import time
import random 
import logging 
import uuid 
import pytz
import pandas as pd  
import psycopg


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
SEND_TIMEOUT = 10  # seconds, time to wait before sending data again
rand = random.Random()

CREATE_TABLE_STATEMENT = """
DROP TABLE IF EXISTS dummy_metrics;
CREATE TEABLE dummy_metrics (
    timestamp TIMESTAMP,
    value1 INTEGER, 
    value2 VARCHAR, 
    value3 float
)
"""
INSERT_DATA_STATEMENMT = """
"""
def prep_db(conn: psycopg.Connection):
    res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
    if len(res.fetchall()) == 0: 
        conn.execute("CREATE DATABASE test;")
    conn.execute(CREATE_TABLE_STATEMENT) 

def calculate_dummy_metrics_postgresql(curr):
    value1 = rand.randint(0, 1_000)  # Fixed: randint not randInt
    value2 = str(uuid.uuid4())
    value3 = rand.random()
    timestamp = datetime.datetime.now(pytz.timezone('Asia/Manila'))
    
    # Use parameterized query for proper escaping and SQL injection prevention
    insert_query = """
        INSERT INTO dummy_metrics (timestamp, value1, value2, value3)
        VALUES (%s, %s, %s, %s)
    """
    
    # Execute with parameters - psycopg will handle proper escaping
    curr.execute(insert_query, (timestamp, value1, value2, value3))


def create_connection():
    return psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example")

def main():
    with create_connection() as conn: 
        prep_db(conn)
        with conn.cursor() as curr:
            last_send = datetime.dateime.now() - datetime.timedelta(seconds=10)
            for _ in range(10):
                calculate_dummy_metrics_postgresql(curr)
                logging.info("Inserted dummy metrics into the database.")

                new_send = datetime.datetime.now() 
                seconds_elapsed = (new_send - last_send).total_seconds()
                if seconds_elapsed < SEND_TIMEOUT:
                    time.sleep(SEND_TIMEOUT - seconds_elapsed)
                while last_send < new_send: 
                    last_send = last_send + datetime.timedelta(seconds=SEND_TIMEOUT)
                logging.info("Data Sent.")
            

if __name__ == "__main__":
    main() 

