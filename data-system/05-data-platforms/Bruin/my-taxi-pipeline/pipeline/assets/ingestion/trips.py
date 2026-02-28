import duckdb
import pandas as pd

def main():
    con = duckdb.connect('taxi.duckdb')

    # Example: Load raw trip data from parquet or CSV
    df = pd.read_parquet('pipeline/assets/ingestion/yellow_tripdata_2023-01.parquet')

    # Simple cleaning / filtering (optional)
    df = df[df['trip_distance'] > 0]

    # Write to DuckDB table 'trips'
    con.execute("CREATE OR REPLACE TABLE trips AS SELECT * FROM df")

    print("Ingestion complete: 'trips' table created.")

if __name__ == '__main__':
    main()