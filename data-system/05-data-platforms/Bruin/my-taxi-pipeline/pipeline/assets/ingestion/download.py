import requests

URL = "https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_2023-01.parquet"

r = requests.get(URL)

with open("yellow_tripdata_2023-01.parquet", "wb") as f:
    f.write(r.content)

print("Download complete")