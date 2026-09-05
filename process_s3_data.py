from pathlib import Path

from src.config import (
    AWS_REGION,
    S3_BUCKET_NAME,
    S3_RAW_PREFIX,
    S3_PROCESSED_PREFIX,
)
from src.ingestion.csv_ingestion import load_csv
from src.storage.s3 import S3Storage
from src.transformation.etl import transform


def main():
    storage = S3Storage(
        bucket_name=S3_BUCKET_NAME,
        region_name=AWS_REGION,
    )

    raw_key = f"{S3_RAW_PREFIX}customers.csv"
    processed_key = f"{S3_PROCESSED_PREFIX}customers_processed.csv"

    raw_file = Path("data/raw/customers.csv")
    processed_file = Path("data/processed/customers_processed.csv")

    raw_file.parent.mkdir(parents=True, exist_ok=True)
    processed_file.parent.mkdir(parents=True, exist_ok=True)

    print("Downloading raw data from S3...")

    storage.download_file(
        s3_key=raw_key,
        local_path=str(raw_file),
    )

    print(f"Downloaded: s3://{S3_BUCKET_NAME}/{raw_key}")

    print("Loading CSV...")

    dataframe = load_csv(str(raw_file))

    print(f"Loaded {len(dataframe)} rows.")

    print("Transforming data...")

    transformed_dataframe = transform(dataframe)

    print(
        f"Transformation complete. "
        f"{len(transformed_dataframe)} clean rows remain."
    )

    print("Saving processed data locally...")

    transformed_dataframe.to_csv(
        processed_file,
        index=False,
    )

    print(f"Saved: {processed_file}")

    print("Uploading processed data to S3...")

    storage.upload_file(
        local_path=str(processed_file),
        s3_key=processed_key,
    )

    print(
        f"SUCCESS: Uploaded processed data to "
        f"s3://{S3_BUCKET_NAME}/{processed_key}"
    )


if __name__ == "__main__":
    main()
    