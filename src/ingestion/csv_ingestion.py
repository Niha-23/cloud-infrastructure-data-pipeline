from pathlib import Path

import pandas as pd

from src.logger import get_logger


logger = get_logger(__name__)


def load_csv(file_path: str) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {file_path}"
        )

    logger.info(
        "Loading CSV file: %s",
        file_path,
    )

    dataframe = pd.read_csv(path)

    logger.info(
        "Loaded %s rows and %s columns",
        len(dataframe),
        len(dataframe.columns),
    )

    return dataframe