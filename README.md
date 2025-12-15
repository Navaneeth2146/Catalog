# Catalog

A FastAPI service that upload product catalog data from CSV , validates it, and performs read/search APIs with database as PostgreSQL via SQLAlchemy.

## Features
- Upload a CSV file to `/products/upload` and insert only valid rows; invalid ones are returned with reasons.
- Paginated listing using `GET /products?page=<n>&limit=<m>`.
- Filter by brand, color, or price range using `GET /products/search`.
- Works locally with Python or end-to-end through Docker Compose (API + Postgres).

## Requirements
- Python 3.11+
- PostgreSQL (local) and Docker/Docker Compose
- Set `DATABASE_URL` as env variable 

## Local Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql://postgres:postgre@localhost:5432/catalog"
uvicorn app.main:app --reload
```
The API runs on `http://127.0.0.1:8000` with the interactive docs at `/docs`.

## Docker Setup
```bash
docker compose up --build
```
This starts a Postgres container and the FastAPI app.

## CSV Format
Required fields: `sku,name,brand,mrp,price,quantity`. Optional fields include `color`, `size`. 
Rows failing validation are given as error.

`sample.csv` is the implied data file.

## API Overview

### POST `/products/upload`
Multipart form upload (field name `file`) with `text/csv` file. Response example:
```json
{
  "msg": "DATA PARTIALLY INSERTED",
  "success": 8,
  "failure": 2,
  "errors": [
    {
      "row": {"sku": "PRD010", "...": "..."},
      "errors": [{"type": "missing_fields", "fields": ["price"]}]
    }
  ]
}
```

### GET `/products`
Query params: `page` and `limit`. Returns `total`, `pages`, and `data` array.

### GET `/products/search`
Optional query params `brand`, `color`, `minprice`, `maxprice`. Returns matching products only.

## TESTING Instructions
Tests folder contains the test files.
Test is executed by running "pytest" command.