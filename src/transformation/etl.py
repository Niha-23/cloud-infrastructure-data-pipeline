import pandas as pd

from src.logger import get_logger


logger = get_logger(__name__)


REQUIRED_COLUMNS = {
    "customer_id",
    "name",
    "email",
    "country",
    "signup_date",
    "spend",
}


def validate_columns(
    dataframe: pd.DataFrame,
) -> None:
    """Validate that required columns exist."""

    missing = REQUIRED_COLUMNS - set(
        dataframe.columns
    )

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )


def transform(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Clean and transform customer data."""

    logger.info("Starting transformation")

    validate_columns(dataframe)

    result = dataframe.copy()

    result["email"] = (
        result["email"]
        .str.lower()
        .str.strip()
    )

    result["name"] = (
        result["name"]
        .str.strip()
    )

    result["country"] = (
        result["country"]
        .str.strip()
    )

    result["signup_date"] = pd.to_datetime(
        result["signup_date"],
        errors="coerce",
    )

    result["spend"] = pd.to_numeric(
        result["spend"],
        errors="coerce",
    )

    result = result.drop_duplicates(
        subset=["customer_id"]
    )

    result = result.dropna(
        subset=[
            "customer_id",
            "email",
            "signup_date",
            "spend",
        ]
    )

    result["customer_segment"] = pd.cut(
        result["spend"],
        bins=[
            -1,
            500,
            1000,
            2000,
            float("inf"),
        ],
        labels=[
            "Low",
            "Medium",
            "High",
            "Premium",
        ],
    )

    logger.info(
        "Transformation completed. %s clean rows remain.",
        len(result),
    )

    return result