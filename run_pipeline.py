from pathlib import Path

from src.config import (
    AWS_REGION,
    S3_BUCKET_NAME,
    S3_RAW_PREFIX,
    S3_PROCESSED_PREFIX,
)
from src.ingestion.csv_ingestion import load_csv
from src.logger import get_logger
from src.storage.s3 import S3Storage
from src.transformation.etl import transform


logger = get_logger(__name__)


def run_pipeline():
    """Run the complete customer data ETL pipeline."""

    logger.info("Starting customer data pipeline.")

    storage = S3Storage(
        bucket_name=S3_BUCKET_NAME,
        region_name=AWS_REGION,
    )

    # ---------------------------------------------------------
    # 1. Define file locations
    # ---------------------------------------------------------

    local_input = Path("sample_data/customers.csv")

    raw_local = Path("data/raw/customers.csv")

    processed_local = Path(
        "data/processed/customers_processed.csv"
    )

    raw_s3_key = f"{S3_RAW_PREFIX}customers.csv"

    processed_s3_key = (
        f"{S3_PROCESSED_PREFIX}customers_processed.csv"
    )

    # ---------------------------------------------------------
    # 2. Validate local input
    # ---------------------------------------------------------

    if not local_input.exists():
        raise FileNotFoundError(
            f"Input file not found: {local_input}"
        )

    # ---------------------------------------------------------
    # 3. Upload raw data to S3
    # ---------------------------------------------------------

    logger.info("Uploading raw data to S3.")

    storage.upload_file(
        local_path=str(local_input),
        s3_key=raw_s3_key,
    )

    # ---------------------------------------------------------
    # 4. Download raw data from S3
    # ---------------------------------------------------------

    raw_local.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger.info("Downloading raw data from S3.")

    storage.download_file(
        s3_key=raw_s3_key,
        local_path=str(raw_local),
    )

    # ---------------------------------------------------------
    # 5. Load raw CSV
    # ---------------------------------------------------------

    dataframe = load_csv(
        str(raw_local)
    )

    # ---------------------------------------------------------
    # 6. Transform data
    # ---------------------------------------------------------

    logger.info(
        "Transforming %s rows.",
        len(dataframe),
    )

    transformed_dataframe = transform(
        dataframe
    )

    # ---------------------------------------------------------
    # 7. Save processed data locally
    # ---------------------------------------------------------

    processed_local.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    transformed_dataframe.to_csv(
        processed_local,
        index=False,
    )

    logger.info(
        "Saved processed data to %s.",
        processed_local,
    )

    # ---------------------------------------------------------
    # 8. Upload processed data to S3
    # ---------------------------------------------------------

    logger.info(
        "Uploading processed data to S3."
    )

    storage.upload_file(
        local_path=str(processed_local),
        s3_key=processed_s3_key,
    )

    # ---------------------------------------------------------
    # 9. Pipeline summary
    # ---------------------------------------------------------

    logger.info(
        "Pipeline completed successfully."
    )

    logger.info(
        "Input rows: %s",
        len(dataframe),
    )

    logger.info(
        "Output rows: %s",
        len(transformed_dataframe),
    )

    logger.info(
        "Processed file: s3://%s/%s",
        S3_BUCKET_NAME,
        processed_s3_key,
    )


if __name__ == "__main__":
    run_pipeline()