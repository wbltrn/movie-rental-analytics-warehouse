"""
Extract data from source systems.

Sources:
- MySQL Sakila database
- CSV promotion dataset
- MongoDB loyalty collection
"""

from __future__ import annotations

import os
from typing import Any, Dict

import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient


def get_mysql_engine():
    """
    Create a SQLAlchemy engine for the Sakila MySQL database.

    Expected environment variables:
    - MYSQL_USER
    - MYSQL_PASSWORD
    - MYSQL_HOST
    - MYSQL_PORT
    - MYSQL_DATABASE
    """
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    host = os.getenv("MYSQL_HOST", "localhost")
    port = os.getenv("MYSQL_PORT", "3306")
    database = os.getenv("MYSQL_DATABASE", "sakila")

    connection_string = (
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    )
    return create_engine(connection_string)


def extract_mysql_data(engine) -> Dict[str, pd.DataFrame]:
    """
    Extract source tables from the Sakila relational database.
    """
    queries = {
        "payment": "SELECT * FROM payment",
        "rental": "SELECT * FROM rental",
        "inventory": "SELECT * FROM inventory",
        "customer": "SELECT * FROM customer",
        "film": "SELECT * FROM film",
        "store": "SELECT * FROM store",
        "staff": "SELECT * FROM staff",
        "address": "SELECT * FROM address",
        "city": "SELECT * FROM city",
        "country": "SELECT * FROM country",
    }

    data = {}
    for table_name, query in queries.items():
        data[table_name] = pd.read_sql(query, engine)

    return data


def extract_csv_data(csv_path: str = "data/promotion_calendar.csv") -> pd.DataFrame:
    """
    Extract promotion data from a CSV file.

    If the file does not exist yet, return an empty DataFrame so the
    pipeline can still run while development is in progress.
    """
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)

    return pd.DataFrame(
        columns=[
            "promo_id",
            "promo_name",
            "start_date",
            "end_date",
            "discount_type",
            "discount_percent",
            "category_name",
        ]
    )


def extract_mongo_data() -> pd.DataFrame:
    """
    Extract loyalty data from MongoDB.

    Expected environment variables:
    - MONGO_URI
    - MONGO_DB
    - MONGO_COLLECTION
    """
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    mongo_db = os.getenv("MONGO_DB", "movie_rental_aux")
    mongo_collection = os.getenv("MONGO_COLLECTION", "customer_loyalty")

    try:
        client = MongoClient(mongo_uri)
        collection = client[mongo_db][mongo_collection]
        docs = list(collection.find())

        if not docs:
            return pd.DataFrame(
                columns=[
                    "customer_id",
                    "loyalty_tier",
                    "preferred_genre",
                    "signup_channel",
                    "is_marketing_opt_in",
                ]
            )

        df = pd.DataFrame(docs)

        if "_id" in df.columns:
            df = df.drop(columns=["_id"])

        return df

    except Exception:
        return pd.DataFrame(
            columns=[
                "customer_id",
                "loyalty_tier",
                "preferred_genre",
                "signup_channel",
                "is_marketing_opt_in",
            ]
        )


def extract_data() -> Dict[str, Any]:
    """
    Main extraction function for all source systems.
    """
    engine = get_mysql_engine()
    mysql_data = extract_mysql_data(engine)
    promotions_df = extract_csv_data()
    loyalty_df = extract_mongo_data()

    return {
        "mysql": mysql_data,
        "promotions": promotions_df,
        "loyalty": loyalty_df,
    }


if __name__ == "__main__":
    extracted = extract_data()

    print("Extraction complete.")
    print("\nMySQL tables extracted:")
    for name, df in extracted["mysql"].items():
        print(f"- {name}: {df.shape}")

    print(f"\nPromotions CSV shape: {extracted['promotions'].shape}")
    print(f"Loyalty MongoDB shape: {extracted['loyalty'].shape}")
