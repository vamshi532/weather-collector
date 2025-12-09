# Weather Data Collection System

A real-time weather data ingestion system that follows DevOps best practices by integrating:

- **External API Integration** (OpenWeather API)
- **Cloud Storage** (AWS S3)
- **Infrastructure as Code** (Terraform)
- **Continuous Integration** (GitHub Actions)
- **Python Development** with environment-based configuration
- **Secure Credential Management** using GitHub Secrets

This project automatically collects weather data for multiple cities, timestamps each entry, and stores it in Amazon S3 for historical analysis.

---

## Repository Link  
**GitHub:** https://github.com/vamshi532/weather-collector

---

## Features

✔ Fetches real-time weather data from OpenWeather API  
✔ Supports multiple cities  
✔ Stores timestamped weather metrics (temperature, humidity, conditions)  
✔ Maintains historical folder structure:

## s3://your-bucket-name/<CITY>/<YYYY>/<MM>/<DD>/<timestamp>.json

✔ Error handling and retries  
✔ Runs automatically via GitHub Actions schedule  
✔ Terraform configuration to provision S3 bucket

## Project Structure

weather-collector/
├── src/
│ ├── weather_collector.py
│ ├── requirements.txt
│ ├── .env.example
│ └── cities.txt
├── terraform/
│ ├── main.tf
│ ├── variables.tf
│ └── outputs.tf
├── .github/
│ └── workflows/
│ └── scheduled-collect.yml
└── README.md

## Local Setup

1️.Clone repository
git clone https://github.com/vamshi532/weather-collector.git
cd weather-collector/src

2️ Create a virtual environment
python3 -m venv venv
source venv/bin/activate

3️ Install dependencies
pip install -r requirements.txt

4️ Create your .env
cp .env.example .env


## Fill the values:

OPENWEATHER_API_KEY=your_key
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_key
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET_NAME=vamshi-149916142189-weather-01
CITIES=London,New_York,Hyderabad

5️ Run locally
python weather_collector.py

## AWS S3 Structure Example
s3://vamshi-149916142189-weather-01/
└── Hyderabad/
    └── 2025/
        └── 12/
            └── 09/
                ├── 101542.json
                ├── 102737.json
                └── 112915.json


Each JSON contains:

{
  "city": "New York",
  "timestamp": "2025-12-09T11:29:15.600958+00:00",
  "temp_f": 21.43,
  "humidity": 49,
  "conditions": "clear sky",
  "raw": {... full OpenWeather payload ...}
}

## Terraform (Infrastructure as Code)

Terraform module is found in terraform/.

Initialize:
cd terraform
terraform init

Apply:
terraform apply -var "bucket_name=<your_bucket>" -auto-approve

If bucket already exists:
terraform import aws_s3_bucket.weather_bucket <bucket_name>

## GitHub Actions (Scheduled Collector)

The workflow .github/workflows/scheduled-collect.yml:
Runs every 6 hours
Installs Python dependencies
Reads GitHub Secrets
Runs python src/weather_collector.py
Uploads new weather data to S3

## Required GitHub Secrets
Secret Name	Description
OPENWEATHER_API_KEY	OpenWeather API key
AWS_ACCESS_KEY_ID	IAM access key
AWS_SECRET_ACCESS_KEY	IAM secret
AWS_DEFAULT_REGION	E.g., us-east-1
S3_BUCKET_NAME	Your bucket
CITIES	City list
✔ Verification Steps
Check S3:
aws s3 ls s3://your-bucket --recursive | tail -n 20

Download latest file:
latest=$(aws s3 ls s3://your-bucket --recursive | sort | tail -n 1 | awk '{print $4}')
aws s3 cp s3://your-bucket/$latest latest.json
cat latest.json

## Future Enhancements (optional)

Replace IAM keys with GitHub OIDC (no long-lived secrets)
Add DynamoDB indexing for fast querying
Build dashboard to visualize weather trends
Add retry + dead-letter queue (SQS)

## Author

Vamshi
Weather Collector — DevOps Automation Project