import requests
import json

def fetch_air_quality_data():
    url = "https://api.openaq.org/v1/measurements"
    params = {
        "parameter": "pm25",  # Example parameter (particulate matter)
        "limit": 1000  # Adjust as needed
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get('results', []) 

def save_to_s3(data, s3_bucket, s3_key):
    s3_path = f"s3://{s3_bucket}/{s3_key}"
    with open(s3_path, "w") as f:
        json.dump(data, f)

def ingest_air_quality_data():
    air_quality_data = fetch_air_quality_data()
    save_to_s3(air_quality_data, "dataminded-academy-capstone-resources/bo/ingest/", "air_quality_data.json")
