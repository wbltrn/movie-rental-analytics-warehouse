"""
Main ETL pipeline orchestrating extract, transform, and load steps.
"""

from extract import extract_data
from transform import transform_data
from load import load_data

def run_pipeline():
    data = extract_data()
    transformed = transform_data(data)
    load_data(transformed)

if __name__ == "__main__":
    run_pipeline()
