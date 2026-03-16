"""
Load transformed data into the movie rental data warehouse.
"""

import os
import pandas as pd
from sqlalchemy import create_engine

def get_dw_engine():

    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    host = os.getenv("MYSQL_HOST")
    port = os.getenv("MYSQL_PORT")
    database = "movie_rental_dw"

    connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

    return create_engine(connection_string)


def load_tables(dim_customer,
                dim_film,
                dim_store,
                dim_staff,
                fact_rental_payment):

    engine = get_dw_engine()

    print("Loading dimension tables...")

    dim_customer.to_sql(
        "dim_customer",
        engine,
        if_exists="replace",
        index=False
    )

    dim_film.to_sql(
        "dim_film",
        engine,
        if_exists="replace",
        index=False
    )

    dim_store.to_sql(
        "dim_store",
        engine,
        if_exists="replace",
        index=False
    )

    dim_staff.to_sql(
        "dim_staff",
        engine,
        if_exists="replace",
        index=False
    )

    print("Loading fact table...")

    fact_rental_payment.to_sql(
        "fact_rental_payment",
        engine,
        if_exists="replace",
        index=False
    )

    print("Data successfully loaded into warehouse.")