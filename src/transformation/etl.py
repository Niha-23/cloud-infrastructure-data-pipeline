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


def validate_columns(dataframe: pd.DataFrame) -> None:
    """Validate that required columns exist."""

    missing = REQUIRED_COLUMNS - set(dataframe.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )


def validate_email_format(dataframe: pd.DataFrame) -> None:
    """Validate that customer email addresses follow a basic format."""

    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    invalid_emails = ~dataframe["email"].astype(str).str.match(
        email_pattern,
        na=False,
    )

    invalid_count = invalid_emails.sum()

    if invalid_count > 0:
        logger.warning(
            "Found %s records with invalid email format.",
            invalid_count,
        )


def validate_spend(dataframe: pd.DataFrame) -> None:
    """Validate that customer spending values are not negative."""

    negative_spend = dataframe["spend"] < 0

    invalid_count = negative_spend.sum()

    if invalid_count > 0:
        logger.warning(
            "Found %s records with negative spend values.",
            invalid_count,
        )


def transform(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform customer data."""

    logger.info(
        "Starting transformation with %s input rows.",
        len(dataframe),
    )

    # Validate required columns before processing
    validate_columns(dataframe)

    # Create a copy so the original dataframe is not modified
    result = dataframe.copy()

    # Standardize text fields
    result["email"] = (
        result["email"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    result["name"] = (
        result["name"]
        .astype(str)
        .str.strip()
    )

    result["country"] = (
        result["country"]
        .astype(str)
        .str.strip()
    )

    # Convert signup date to datetime
    result["signup_date"] = pd.to_datetime(
        result["signup_date"],
        errors="coerce",
    )

    # Convert spend to numeric
    result["spend"] = pd.to_numeric(
        result["spend"],
        errors="coerce",
    )

    # Run data-quality validations
    validate_email_format(result)
    validate_spend(result)

    # Remove duplicate customers
    result = result.drop_duplicates(
        subset=["customer_id"]
    )

    # Remove records with missing required values
    result = result.dropna(
        subset=[
            "customer_id",
            "email",
            "signup_date",
            "spend",
        ]
    )

    # Remove negative spending records
    result = result[result["spend"] >= 0]

    # Create customer spending segments
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
        "Transformation completed. %s clean rows remain from %s input rows.",
        len(result),
        len(dataframe),
    )

    return result