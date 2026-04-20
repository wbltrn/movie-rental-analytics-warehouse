# Movie Rental Analytics Data Warehouse

This project builds a data warehouse and ETL pipeline using the **Sakila movie rental database**.  
The goal is to transform transactional (OLTP) data into an analytical star schema that supports business intelligence queries.

The ETL pipeline extracts data from the Sakila database, transforms it into dimension and fact tables, and loads it into a data warehouse for analytics.


## Architecture

Source System:
- MySQL Sakila Database (OLTP)

ETL Pipeline:
- Python scripts for extraction, transformation, and loading

Data Warehouse:
- MySQL star schema

Workflow:

Sakila Database → Extract → Transform → Load → Movie Rental Data Warehouse


## Data Warehouse Schema

The warehouse follows a **star schema** design.

Fact Table:
- `fact_rental_payment` — records rental transactions and payments

Dimension Tables:
- `dim_customer` — customer information
- `dim_film` — film metadata
- `dim_store` — store location details
- `dim_staff` — staff members handling rentals


## ETL Pipeline

The ETL process is implemented in Python.

Scripts:

- `extract.py`  
  Connects to the Sakila database and retrieves raw transactional tables.

- `transform.py`  
  Cleans and transforms data into dimension and fact tables.

- `load.py`  
  Loads the transformed tables into the data warehouse.

- `etl_pipeline.py`  
  Runs the full ETL process.


## Analytical Queries

SQL queries for business analytics are included in:

sql/analytical_queries.sql

Examples include:

- Total revenue analysis
- Revenue by store location
- Top performing films
- Late rental analysis by country


## Repository Structure

```
movie-rental-analytics-warehouse
│
├── data
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
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── etl_pipeline.py
│   └── README.md
│
├── LICENSE
└── README.md
```
---

## Capstone Extension: Multi-Source Lakehouse Pipeline

This project has been extended from a traditional batch ETL data warehouse into a multi-source, streaming-enabled data pipeline.

The goal of the capstone is to demonstrate how data from multiple platforms can be integrated into a single analytical system using business keys and modern data engineering practices.

### Updated Architecture

The pipeline now incorporates multiple data sources and a streaming workflow:

**Data Sources:**
- MySQL (Sakila) — core transactional and dimension data
- MongoDB — semi-structured customer loyalty data (JSON-based)
- CSV Files — external/reference data exported from MySQL
- JSON Files — streaming simulation for fact table data

**Processing Framework:**
- Databricks / Apache Spark
- Structured Streaming (AutoLoader)
- Delta Lake (Bronze, Silver, Gold layers)

**Updated Workflow:**

MySQL / MongoDB / CSV / JSON  
→ Bronze (raw ingestion)  
→ Silver (cleaned + transformed data)  
→ Gold (analytics-ready tables)  

---

### Dimensional Model (Extended)

**Fact Table:**
- `fact_rental_payment` — streaming ingestion of rental transactions

**Dimension Tables:**
- `dim_date` — date dimension
- `dim_customer` — customer data (MySQL)
- `dim_film` — film metadata (MySQL)
- `dim_customer_loyalty` — customer loyalty data (MongoDB)
- `dim_[CSV dimension]` — additional dimension from CSV

---

### Cross-Source Integration

All data sources are integrated using shared business keys:

- `customer_id` links:
  - fact_rental_payment
  - dim_customer
  - dim_customer_loyalty (MongoDB)

- `film_id` links:
  - fact_rental_payment
  - dim_film
  - CSV-based dimension

- `date_key` links:
  - fact_rental_payment
  - dim_date

This ensures that all datasets "talk to each other" and represent a single cohesive business process.

---

### Streaming Pipeline (New)

The fact table is no longer loaded in batch form.

Instead:
- Rental/payment data is exported into multiple JSON files
- These files simulate real-time incoming data
- Spark Structured Streaming ingests this data into:

**Bronze Layer:**
- Raw JSON ingestion

**Silver Layer:**
- Data cleaning and transformation
- Derived fields (rental_days, days_late, is_late)

**Gold Layer:**
- Final fact table joined with all dimensions
- Analytics-ready dataset

---

### Project Goal (Capstone)

This extended pipeline demonstrates:
- Integration of structured and semi-structured data
- Use of multiple storage systems (MySQL, MongoDB, file-based)
- Real-time/streaming data processing
- Transition from traditional ETL to modern lakehouse architecture
