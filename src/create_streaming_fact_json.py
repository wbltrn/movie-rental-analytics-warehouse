import os
import math
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


# Extract fact-style transactional data
query = """
SELECT
    r.rental_id,
    p.payment_id,
    r.customer_id,
    r.staff_id,
    r.inventory_id,
    i.film_id,
    r.rental_date,
    r.return_date,
    p.payment_date,
    p.amount
FROM rental r
JOIN payment p
    ON r.rental_id = p.rental_id
JOIN inventory i
    ON r.inventory_id = i.inventory_id
ORDER BY p.payment_date, r.rental_id
"""

fact_df = pd.read_sql(query, engine)


# Create output directory
output_dir = os.path.join("data", "streaming_input")
os.makedirs(output_dir, exist_ok=True)


# Split into 3 roughly equal JSON files
num_files = 3
chunk_size = math.ceil(len(fact_df) / num_files)

for i in range(num_files):
    start_idx = i * chunk_size
    end_idx = min((i + 1) * chunk_size, len(fact_df))
    chunk = fact_df.iloc[start_idx:end_idx]

    output_path = os.path.join(output_dir, f"fact_rental_payment_part{i+1}.json")

    chunk.to_json(output_path, orient="records", indent=2, date_format="iso")

    print(f"Created: {output_path} with {len(chunk)} records")

print("\nPreview:")
print(fact_df.head())
