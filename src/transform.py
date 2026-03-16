"""
Transform raw source data into dimensional model tables.

Builds:
- dim_customer
- dim_film
- dim_store
- dim_staff
- fact_rental_payment
"""

from __future__ import annotations

from typing import Any, Dict

import numpy as np
import pandas as pd


def _normalize_datetime(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Convert listed columns to pandas datetime when present.
    """
    df = df.copy()
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def build_dim_customer(mysql_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    customer = mysql_data["customer"].copy()
    address = mysql_data["address"].copy()
    city = mysql_data["city"].copy()
    country = mysql_data["country"].copy()

    customer = _normalize_datetime(customer, ["create_date", "last_update"])
    address = _normalize_datetime(address, ["last_update"])
    city = _normalize_datetime(city, ["last_update"])
    country = _normalize_datetime(country, ["last_update"])

    dim_customer = (
        customer.merge(address[["address_id", "city_id"]], on="address_id", how="left")
        .merge(city[["city_id", "city", "country_id"]], on="city_id", how="left")
        .merge(country[["country_id", "country"]], on="country_id", how="left")
    )

    dim_customer = dim_customer[
        [
            "customer_id",
            "first_name",
            "last_name",
            "email",
            "active",
            "create_date",
            "store_id",
            "city",
            "country",
        ]
    ].drop_duplicates(subset=["customer_id"])

    dim_customer = dim_customer.sort_values("customer_id").reset_index(drop=True)
    dim_customer.insert(0, "customer_key", range(1, len(dim_customer) + 1))

    return dim_customer


def build_dim_film(mysql_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    film = mysql_data["film"].copy()

    dim_film = film[
        [
            "film_id",
            "title",
            "release_year",
            "rental_duration",
            "rental_rate",
            "length",
            "replacement_cost",
            "rating",
        ]
    ].drop_duplicates(subset=["film_id"])

    dim_film = dim_film.sort_values("film_id").reset_index(drop=True)
    dim_film.insert(0, "film_key", range(1, len(dim_film) + 1))

    return dim_film


def build_dim_store(mysql_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    store = mysql_data["store"].copy()
    address = mysql_data["address"].copy()
    city = mysql_data["city"].copy()
    country = mysql_data["country"].copy()

    dim_store = (
        store.merge(address[["address_id", "city_id"]], on="address_id", how="left")
        .merge(city[["city_id", "city", "country_id"]], on="city_id", how="left")
        .merge(country[["country_id", "country"]], on="country_id", how="left")
    )

    dim_store = dim_store[
        [
            "store_id",
            "manager_staff_id",
            "city",
            "country",
        ]
    ].drop_duplicates(subset=["store_id"])

    dim_store = dim_store.sort_values("store_id").reset_index(drop=True)
    dim_store.insert(0, "store_key", range(1, len(dim_store) + 1))

    return dim_store


def build_dim_staff(mysql_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    staff = mysql_data["staff"].copy()
    staff = _normalize_datetime(staff, ["last_update"])

    dim_staff = staff[
        [
            "staff_id",
            "first_name",
            "last_name",
            "email",
            "active",
            "username",
            "store_id",
        ]
    ].drop_duplicates(subset=["staff_id"])

    dim_staff = dim_staff.sort_values("staff_id").reset_index(drop=True)
    dim_staff.insert(0, "staff_key", range(1, len(dim_staff) + 1))

    return dim_staff


def build_fact_rental_payment(
    mysql_data: Dict[str, pd.DataFrame],
    dim_customer: pd.DataFrame,
    dim_film: pd.DataFrame,
    dim_store: pd.DataFrame,
    dim_staff: pd.DataFrame,
) -> pd.DataFrame:
    payment = mysql_data["payment"].copy()
    rental = mysql_data["rental"].copy()
    inventory = mysql_data["inventory"].copy()
    film = mysql_data["film"].copy()

    payment = _normalize_datetime(payment, ["payment_date", "last_update"])
    rental = _normalize_datetime(rental, ["rental_date", "return_date", "last_update"])

    fact = (
        payment.merge(
            rental[["rental_id", "rental_date", "return_date", "inventory_id"]],
            on="rental_id",
            how="left",
        )
        .merge(
            inventory[["inventory_id", "film_id", "store_id"]],
            on="inventory_id",
            how="left",
        )
        .merge(
            film[["film_id", "rental_duration"]],
            on="film_id",
            how="left",
            suffixes=("", "_film"),
        )
    )

    # date_key from payment_date in YYYYMMDD format
    fact["date_key"] = fact["payment_date"].dt.strftime("%Y%m%d")
    fact["date_key"] = pd.to_numeric(fact["date_key"], errors="coerce").astype("Int64")

    # rental_days
    fact["rental_days"] = (
        fact["return_date"] - fact["rental_date"]
    ).dt.total_seconds() / (60 * 60 * 24)

    fact["rental_days"] = fact["rental_days"].fillna(0).round().astype(int)

    # days_late
    fact["days_late"] = np.maximum(
        fact["rental_days"] - fact["rental_duration"].fillna(0).astype(int),
        0,
    )

    fact["is_late"] = (fact["days_late"] > 0).astype(int)

    # map natural keys to surrogate keys
    fact = fact.merge(
        dim_customer[["customer_key", "customer_id"]],
        on="customer_id",
        how="left",
    )

    fact = fact.merge(
        dim_film[["film_key", "film_id"]],
        on="film_id",
        how="left",
    )

    fact = fact.merge(
        dim_store[["store_key", "store_id"]],
        on="store_id",
        how="left",
    )

    fact = fact.merge(
        dim_staff[["staff_key", "staff_id"]],
        on="staff_id",
        how="left",
    )

    fact_rental_payment = fact[
        [
            "payment_id",
            "rental_id",
            "date_key",
            "customer_key",
            "film_key",
            "store_key",
            "staff_key",
            "amount",
            "rental_days",
            "days_late",
            "is_late",
        ]
    ].copy()

    fact_rental_payment = fact_rental_payment.rename(
        columns={"amount": "payment_amount"}
    )

    fact_rental_payment = fact_rental_payment.sort_values("payment_id").reset_index(
        drop=True
    )
    fact_rental_payment.insert(
        0, "fact_rental_payment_key", range(1, len(fact_rental_payment) + 1)
    )

    return fact_rental_payment


def transform_data(extracted_data: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    """
    Main transformation function.
    """
    mysql_data = extracted_data["mysql"]

    dim_customer = build_dim_customer(mysql_data)
    dim_film = build_dim_film(mysql_data)
    dim_store = build_dim_store(mysql_data)
    dim_staff = build_dim_staff(mysql_data)

    fact_rental_payment = build_fact_rental_payment(
        mysql_data=mysql_data,
        dim_customer=dim_customer,
        dim_film=dim_film,
        dim_store=dim_store,
        dim_staff=dim_staff,
    )

    return {
        "dim_customer": dim_customer,
        "dim_film": dim_film,
        "dim_store": dim_store,
        "dim_staff": dim_staff,
        "fact_rental_payment": fact_rental_payment,
    }


if __name__ == "__main__":
    from extract import extract_data

    extracted = extract_data()
    transformed = transform_data(extracted)

    print("Transformation complete.\n")
    for name, df in transformed.items():
        print(f"{name}: {df.shape}")
        print(df.head(), "\n")