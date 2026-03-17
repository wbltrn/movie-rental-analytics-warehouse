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
│   └── star_schema_movie_rental.svg
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
│   └── etl_pipeline.py
│
├── LICENSE
└── README.md
```
