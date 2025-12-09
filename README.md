# Weather Data Collection System

This repo contains:
- Python collector (`src/weather_collector.py`) pulling OpenWeather data, saving timestamped JSON objects to S3.
- Terraform to create/manage the S3 bucket (`terraform/`).
- GitHub Actions workflow to run the collector on a schedule (`.github/workflows/scheduled-collect.yml`).
- Architecture diagram (Mermaid) included in this repo.

Run locally:
1. cd src
2. python3 -m venv venv && source venv/bin/activate
3. pip install -r requirements.txt
4. copy `.env.example` to `.env` and fill keys
5. python weather_collector.py

Do NOT commit secrets. Use GitHub Secrets for CI.
