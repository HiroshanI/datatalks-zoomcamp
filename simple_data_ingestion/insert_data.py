#!/usr/bin/env python

import os
import argparse
from time import time

import pandas as pd
from sqlalchemy import create_engine


def main(args):
    """
    Main function
    """
    conn_str = f"postgresql://{args.user}:{args.password}@{args.host}:{args.port}/{args.dbname}"
    engine = create_engine(conn_str)

    os.system(f"wget {args.url} -O data.csv.gz")
    os.system(f"gzip -d data.csv.gz")

    df_iter = pd.read_csv(
        'data.csv', 
        iterator=True, 
        chunksize=100000,
        parse_dates=['tpep_pickup_datetime', 'tpep_dropoff_datetime'],
        low_memory=False,
        nrows=398161
    )

    print("\n~~ Started Inserting Data ~~\n")
    total_rows, total_time = 0,0
    for i, df in enumerate(df_iter, 1):
        start_time = time()
        if i == 1:
            df.head(0).to_sql(name=args.tablename, con=engine, if_exists='replace')
        
        df.to_sql(name=args.tablename, con=engine, if_exists='append')
        insert_time = time() - start_time
        total_rows += len(df)
        total_time += insert_time
        print(f"Inserted chunk {i:02d} with {len(df)} rows ... took {insert_time:.2f}s")
    print(f"* Inserted {total_rows} rows ... took {total_time:.2f}s total")
    print("\n~~ Finished Inserting Data ~~\n")


if __name__ == "__main__":
    """
    Example:
    python insert_data.py \
        --user root \
        --port 5432 \
        --password root \
        --dbname ny_taxi \
        --host localhost \
        --tablename yellow_trips \
        --url ./input/yellow_tripdata_2021-01.csv
    """
    parser = argparse.ArgumentParser(description='Insert CSV data into pg table')
    parser.add_argument("--user")
    parser.add_argument("--password")
    parser.add_argument("--host")
    parser.add_argument("--port")
    parser.add_argument("--dbname")
    parser.add_argument("--tablename")
    parser.add_argument("--url", help='url of the input CSV file')

    args = parser.parse_args()

    main(args)


"""
RUN IN DOCKER
docker run -it \
    --network pg-network \
    ingest_data:test_v2 \
        --user root \
        --port 5432 \
        --password root \
        --dbname ny_taxi \
        --host pg-db \
        --tablename yellow_trips \
        --url https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
"""
