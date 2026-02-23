# Nabarangpur Tender Extractor

A Flask website that extracts latest active tender data from `https://tendersodisha.gov.in/nicgep/app` and filters it for **Nabarangpur district**.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`.

## API

- `GET /api/tenders?district=Nabarangpur`

Returns filtered tenders as JSON.
