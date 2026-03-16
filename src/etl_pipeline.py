from extract import extract_data
from transform import transform_data
from load import load_tables


def run_pipeline():

    print("Starting ETL pipeline...")

    extracted = extract_data()

    transformed = transform_data(extracted)

    load_tables(**transformed)

    print("ETL pipeline complete.")


if __name__ == "__main__":
    run_pipeline()