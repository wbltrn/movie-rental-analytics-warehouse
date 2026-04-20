import os
import json
import random
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


# Extract customer base data

query = """
SELECT
    customer_id,
    create_date
FROM customer
"""

customers = pd.read_sql(query, engine)

# Generate loyalty attributes

random.seed(42)

def assign_loyalty_tier(points):
    if points >= 4000:
        return "Platinum"
    elif points >= 2500:
        return "Gold"
    elif points >= 1000:
        return "Silver"
    else:
        return "Bronze"

customers["loyalty_points"] = [
    random.randint(100, 5000) for _ in range(len(customers))
]

customers["loyalty_tier"] = customers["loyalty_points"].apply(assign_loyalty_tier)

customers["member_since"] = pd.to_datetime(customers["create_date"]).dt.strftime("%Y-%m-%d")

customers["is_active_member"] = [
    random.choice([True, True, True, False]) for _ in range(len(customers))
]

# Final loyalty dimension

dim_customer_loyalty = customers[
    ["customer_id", "loyalty_tier", "loyalty_points", "member_since", "is_active_member"]
].copy()

# Save as JSON

output_dir = os.path.join("data", "exports")
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "dim_customer_loyalty.json")

dim_customer_loyalty.to_json(
    output_path,
    orient="records",
    indent=2
)

print(f"Customer loyalty JSON created at: {output_path}")
print(dim_customer_loyalty.head())
