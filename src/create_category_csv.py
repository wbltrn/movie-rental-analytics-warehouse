import os
import pandas as pd
from sqlalchemy import create_engine


# Database connection
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "sakila")

connection_string = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

engine = create_engine(connection_string)


# Extract film-category data

query = """
SELECT
    fc.film_id,
    c.category_id,
    c.name AS category_name
FROM film_category fc
JOIN category c
    ON fc.category_id = c.category_id
ORDER BY fc.film_id
"""

dim_category = pd.read_sql(query, engine)


# Save as CSV

output_dir = os.path.join("data", "exports")
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "dim_category.csv")

dim_category.to_csv(output_path, index=False)

print(f"Category CSV created at: {output_path}")
print(dim_category.head())
