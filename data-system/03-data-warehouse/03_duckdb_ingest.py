import dlt
import requests
import pandas as pd
from io import BytesIO

# Define a dlt resource to download and process Parquet files as single table
@dlt.resource(name="rides", write_disposition="replace")
def download_parquet():
    prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata'
    
    for month in range(1, 7):
        url = f"{prefix}_2024-{month:02d}.parquet"
        
        print(f"  📥 Downloading month {month}...")
        response = requests.get(url, timeout=30)
        df = pd.read_parquet(BytesIO(response.content))
        print(f"     ✓ Loaded {len(df):,} rows")
        
        yield df

# Initialize the pipeline
pipeline = dlt.pipeline(
    pipeline_name="rides_pipeline",
    destination="duckdb",  # Use DuckDB for testing
    # destination="bigquery",  # Use BigQuery for production
    dataset_name="rides_dataset",
)

print("🚀 Running pipeline (loading to DuckDB)...\n")
info = pipeline.run(download_parquet)

print(f"\n✅ Pipeline completed!")
print(f"\n📊 Load Info:\n{info}")