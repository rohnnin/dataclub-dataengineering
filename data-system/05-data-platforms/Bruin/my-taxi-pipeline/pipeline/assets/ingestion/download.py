import requests

URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"

response = requests.get(URL, stream=True)

if response.status_code != 200:
    raise Exception(f"Failed to download file: {response.status_code}")

with open("yellow_tripdata_2023-01.parquet", "wb") as f:
    for chunk in response.iter_content(chunk_size=1024 * 1024):
        if chunk:
            f.write(chunk)

print("Download complete")