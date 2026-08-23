from pathlib import Path

from src.ingestion.csv_ingestion import load_csv
from src.logger import get_logger
from src.transformation.etl import transform


logger = get_logger("pipeline")


INPUT_FILE = "sample_data/customers.csv"

OUTPUT_FILE = (
    "data/processed/customers_processed.csv"
)


def run() -> None:
    """Execute the end-to-end ETL pipeline."""

    logger.info(
        "Starting cloud data pipeline"
    )

    dataframe = load_csv(INPUT_FILE)

    transformed = transform(dataframe)

    Path(
        OUTPUT_FILE
    ).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    transformed.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    logger.info(
        "Processed dataset written to %s",
        OUTPUT_FILE,
    )

    logger.info(
        "Pipeline completed successfully"
    )


if __name__ == "__main__":
    run()