# Movie Rental Analytics Warehouse

This project extends a midterm movie rental data warehouse into a multi-source lakehouse pipeline using Databricks, Delta tables, and medallion architecture.

The project uses the Sakila movie rental database as its core business process and integrates multiple data sources that connect through shared business keys. The final pipeline demonstrates Bronze, Silver, and Gold data layers for analytics-ready reporting.

---

## Project Goal

The goal of this project is to transform transactional movie rental and payment data into a structured analytical pipeline that supports business intelligence and category-level revenue analysis.

This capstone extends the original batch ETL warehouse by incorporating:

- Databricks
- Delta Lake tables
- Medallion Architecture (Bronze, Silver, Gold)
- JSON fact ingestion
- CSV dimension ingestion
- MongoDB-based customer enrichment

---

## Business Process

The business process modeled in this project is movie rental payment activity.

The primary fact data tracks rental and payment transactions, while dimension data enriches those transactions with category and customer-related information.

---

## Data Sources

This project integrates multiple data sources into one analytical workflow.

### 1. MySQL (Sakila)
The Sakila relational database serves as the main operational source system.

Used for:
- rental and payment transaction extraction
- film-related reference data
- generation of exported dimension files

### 2. JSON Files
Fact rental payment data was exported into multiple JSON files to simulate incoming streaming-style transaction batches.

Files created:
- `fact_rental_payment_part1.json`
- `fact_rental_payment_part2.json`
- `fact_rental_payment_part3.json`

These files were uploaded to a Unity Catalog volume in Databricks and used as the Bronze ingestion source.

### 3. CSV File
Category data was exported from Sakila into CSV format.

File created:
- `dim_category.csv`

This file was used as a file-based reference dimension in Databricks.

### 4. MongoDB Atlas
Customer loyalty data was generated from Sakila customer records, exported as JSON, and loaded into MongoDB Atlas.

File created:
- `dim_customer_loyalty.json`

This MongoDB collection represents a semi-structured enrichment source intended to connect to customer-level analytics through `customer_id`.

---

## Architecture

### Original Midterm Architecture
Sakila Database → Python ETL → MySQL Star Schema Warehouse

### Capstone Architecture
JSON / CSV / MySQL / MongoDB  
→ Databricks Ingestion  
→ Bronze Delta Tables  
→ Silver Delta Tables  
→ Gold Delta Tables  
→ Business Insights

---

## Medallion Architecture

### Bronze Layer
Raw rental payment JSON files were ingested from a Unity Catalog volume and stored as a Delta table:

- `fact_rental_payment_bronze`

This layer preserves the raw structure of the ingested transaction data.

### Silver Layer
The Bronze data was cleaned and transformed into a Silver Delta table:

- `fact_rental_payment_silver`

Transformations included:
- schema enforcement
- timestamp conversion
- numeric type casting

### Gold Layer
The Silver table was aggregated into Gold analytics tables:

- `fact_rental_payment_gold`
- `fact_rental_payment_gold_final`

The final Gold layer joined fact data with category information using `film_id` and calculated daily revenue by category.

---

## Tables Created

### Bronze
- `fact_rental_payment_bronze`

### Silver
- `fact_rental_payment_silver`

### Gold
- `fact_rental_payment_gold`
- `fact_rental_payment_gold_final`

### Dimension
- `dim_category`

---

## Final Analytical Output

The final Gold dataset provides daily revenue by film category.

Example columns:
- `payment_day`
- `category_name`
- `total_revenue`

This enables business questions such as:
- Which film categories generate the most revenue?
- How does category revenue change over time?
- Which categories perform best on specific days?

---

## Repository Structure

```text
movie-rental-analytics-warehouse
│
├── data
│   ├── exports
│   │   ├── dim_category.csv
│   │   └── dim_customer_loyalty.json
│   ├── streaming_input
│   │   ├── fact_rental_payment_part1.json
│   │   ├── fact_rental_payment_part2.json
│   │   └── fact_rental_payment_part3.json
│   ├── sakila-data.sql
│   ├── sakila-schema.sql
│   └── README.md
│
├── docs
│   ├── star_schema_movie_rental.svg
│   └── README.md
│
├── sql
│   ├── analytical_queries.sql
│   ├── create_dim_date.sql
│   ├── create_dw_schema.sql
│   └── README.md
│
├── src
│   ├── create_category_csv.py
│   ├── create_customer_loyalty.py
│   ├── create_streaming_fact_json.py
│   ├── etl_pipeline.py
│   ├── extract.py
│   ├── load.py
│   ├── transform.py
│   └── README.md
│
├── LICENSE
└── README.md
