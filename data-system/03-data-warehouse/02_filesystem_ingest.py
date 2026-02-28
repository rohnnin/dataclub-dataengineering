import dlt
import requests
import pandas as pd
from dlt.destinations import filesystem
from io import BytesIO

# Define a dlt source to download and process Parquet files as separate resources
@dlt.source(name="rides")
def download_parquet():
    prefix = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata"
    for month in range(1, 3):  # Start with 2 months for testing
        file_name = f"yellow_tripdata_2024-{month:02d}.parquet"
        url = f"{prefix}_2024-{month:02d}.parquet"
        
        print(f"  📥 Downloading: {file_name}")
        response = requests.get(url)
        df = pd.read_parquet(BytesIO(response.content))
        print(f"     ✓ Got {len(df):,} rows")
        
        yield dlt.resource(df, name=file_name)

# Initialize the pipeline with filesystem destination
pipeline = dlt.pipeline(
    pipeline_name="rides_pipeline_filesystem",
    destination=filesystem(layout="{schema_name}/{table_name}.{ext}"),
    dataset_name="rides_dataset_filesystem",
)

print("🚀 Running pipeline (saves to local files)...")
load_info = pipeline.run(download_parquet(), loader_file_format="parquet")

print("\n✅ Pipeline completed!")
print(f"\n📊 Load Info:\n{load_info}")