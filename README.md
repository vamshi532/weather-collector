# Weather Data Collector

See canvas doc for full instructions. Quickstart:
1. Copy `src/.env.example` to `src/.env` and add keys.
2. Create S3 bucket (we provide Terraform in /terraform).
3. Run locally:
   - python3 -m venv venv
   - source venv/bin/activate
   - pip install -r src/requirements.txt
   - python src/weather_collector.py

Do NOT commit secrets. Use GitHub Secrets for CI.
