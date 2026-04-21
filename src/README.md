# Source Code

This folder contains scripts used to generate and transform data.

## Files
- `extract.py` – extracts data from the Sakila database
- `transform.py` – applies transformations and cleaning
- `load.py` – loads data into target systems
- `etl_pipeline.py` – orchestrates the full ETL workflow

## Additional Scripts
- `create_streaming_fact_json.py` – generates JSON files for Databricks ingestion
- `create_category_csv.py` – exports category dimension as CSV
- `create_customer_loyalty.py` – creates customer loyalty dataset for MongoDB
