import os
import dlt
import requests
import pandas as pd
from io import BytesIO
from dlt.destinations import filesystem

# ================================
# 1. SETUP CREDENTIALS
# ================================

# Uses Codespaces secret
os.environ["DESTINATION__CREDENTIALS"] = os.environ["GCP_CREDENTIALS"]

# Set your bucket here
os.environ["BUCKET_URL"] = "gs://dataclub-s"

# ================================
# 2. SOURCE DEFINITION
# ================================

@dlt.resource(name="rides", write_disposition="replace")
def download_parquet():
    prefix = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata"

    for month in range(1, 7):
        url = f"{prefix}_2024-0{month}.parquet"
        print(f"Downloading {url}")
        response = requests.get(url)
        df = pd.read_parquet(BytesIO(response.content))
        yield df


# ================================
# 3. PIPELINE SETUP
# ================================

pipeline = dlt.pipeline(
    pipeline_name="rides_pipeline",
    destination="duckdb",  # change to "bigquery" if needed
    dataset_name="rides_dataset",
)

# ================================
# 4. RUN PIPELINE
# ================================

info = pipeline.run(download_parquet())

print("Pipeline completed")
print(info)

# ================================
# 5. QUERY RESULT
# ================================

with pipeline.sql_client() as client:
    with client.execute_query("SELECT COUNT(1) FROM rides") as cursor:
        result = cursor.df()

print(result)