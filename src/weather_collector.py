#!/usr/bin/env python3
\"\"\"Weather Data Collector
Fetches current weather for configured cities from OpenWeather (Current Weather API),
creates a timestamped JSON and uploads to S3.
\"\"\"

import os
import json
from datetime import datetime
import requests
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
CITIES_ENV = os.getenv("CITIES")  # comma separated

if not OPENWEATHER_API_KEY:
    raise SystemExit("OPENWEATHER_API_KEY is not set in environment")
if not S3_BUCKET:
    raise SystemExit("S3_BUCKET_NAME is not set in environment")

session = boto3.Session()
s3 = session.client("s3", region_name=AWS_REGION)

API_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_cities():
    # Prefer environment variable CITIES, else cities.txt
    if CITIES_ENV:
        return [c.strip() for c in CITIES_ENV.split(",") if c.strip()]
    try:
        here = os.path.dirname(__file__)
        with open(os.path.join(here, "cities.txt"), "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def fetch_weather(city):
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "imperial"  # Fahrenheit
    }
    try:
        resp = requests.get(API_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        result = {
            "city": city,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "temp_f": data.get("main", {}).get("temp"),
            "humidity": data.get("main", {}).get("humidity"),
            "conditions": data.get("weather", [{}])[0].get("description"),
            "raw": data
        }
        return result
    except requests.RequestException as e:
        print(f"Error fetching {city}: {e}")
        return None

def upload_json(obj, key):
    body = json.dumps(obj).encode("utf-8")
    try:
        s3.put_object(Bucket=S3_BUCKET, Key=key, Body=body, ContentType="application/json")
        print(f"Uploaded {key} to s3://{S3_BUCKET}")
    except ClientError as e:
        print(f"Failed to upload {key}: {e}")

def main():
    cities = get_cities()
    if not cities:
        print("No cities specified. Set CITIES in env or provide src/cities.txt")
        return

    now = datetime.utcnow()
    date_prefix = now.strftime("%Y/%m/%d")
    for city in cities:
        record = fetch_weather(city)
        if not record:
            continue
        city_safe = city.replace(" ", "_")
        time_stamp = now.strftime("%H%M%S")
        key = f"{city_safe}/{date_prefix}/{time_stamp}.json"
        upload_json(record, key)

if __name__ == "__main__":
    main()
