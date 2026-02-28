import dlt
import requests
import pandas as pd
from io import BytesIO
import duckdb

# Define a dlt resource to download and process Parquet files
@dlt.resource(name="rides", write_disposition="replace")
def download_parquet():
    prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata'
    
    # Start with 1 month for testing, increase later
    for month in range(1, 7):  # months 1-1 (January only)
        url = f"{prefix}_2024-0{month}.parquet"
        print(f"Downloading: {url}")
        response = requests.get(url)
        df = pd.read_parquet(BytesIO(response.content))
        print(f"Month {month}: {len(df)} rows loaded")
        yield df


# Initialize the pipeline
pipeline = dlt.pipeline(
    pipeline_name="rides_pipeline",
    destination="duckdb",  # FREE - local database
    dataset_name="rides_dataset",
)

print("Starting pipeline...")
info = pipeline.run(download_parquet)
print(f"Pipeline completed!\n{info}")

# Query the data
print("\n--- Querying Data ---")
conn = duckdb.connect("rides_pipeline.duckdb")
conn.sql(f"SET search_path = 'rides_dataset'")

# Show tables
print("Tables in database:")
tables = conn.sql("DESCRIBE").df()
print(tables)

# Count total rows
result = conn.sql("SELECT count(1) as total_rows FROM rides").df()
print(f"\nTotal rows: {result['total_rows'].values[0]}")

# Show sample data
print("\nSample data (first 5 rows):")
sample = conn.sql("SELECT * FROM rides LIMIT 5").df()
print(sample)